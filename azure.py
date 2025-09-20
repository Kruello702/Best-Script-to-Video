from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
import os
from src.services.azure_integration import AzureIntegrationService

azure_bp = Blueprint('azure', __name__)

@azure_bp.route('/status', methods=['GET'])
@cross_origin()
def get_azure_status():
    """Get the status of Azure integration."""
    try:
        azure_service = AzureIntegrationService()
        status = azure_service.get_configuration_status()
        
        return jsonify({
            'configured': azure_service.is_configured(),
            'services': status
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting Azure status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@azure_bp.route('/setup', methods=['GET'])
@cross_origin()
def get_setup_instructions():
    """Get setup instructions for Azure integration."""
    try:
        azure_service = AzureIntegrationService()
        instructions = azure_service.setup_instructions()
        
        return jsonify(instructions)
        
    except Exception as e:
        current_app.logger.error(f"Error getting setup instructions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@azure_bp.route('/upload', methods=['POST'])
@cross_origin()
def upload_to_azure():
    """Upload a video to Azure Blob Storage."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        video_path = data.get('video_path', '')
        container_name = data.get('container_name', 'videos')
        
        if not video_path:
            return jsonify({'error': 'Video path is required'}), 400
        
        if not os.path.exists(video_path):
            return jsonify({'error': 'Video file not found'}), 404
        
        # Initialize Azure service
        azure_service = AzureIntegrationService()
        
        if not azure_service.is_configured():
            return jsonify({'error': 'Azure services not configured'}), 503
        
        # Upload to Azure Blob Storage
        blob_url = azure_service.upload_video_to_blob(video_path, container_name)
        
        if not blob_url:
            return jsonify({'error': 'Failed to upload video to Azure'}), 500
        
        # Create CDN endpoint for better performance
        cdn_url = azure_service.create_cdn_endpoint(blob_url)
        
        return jsonify({
            'original_path': video_path,
            'blob_url': blob_url,
            'cdn_url': cdn_url,
            'container': container_name,
            'status': 'uploaded'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error uploading to Azure: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@azure_bp.route('/stream', methods=['POST'])
@cross_origin()
def create_streaming_endpoint():
    """Create streaming endpoints for a video."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        video_url = data.get('video_url', '')
        
        if not video_url:
            return jsonify({'error': 'Video URL is required'}), 400
        
        # Initialize Azure service
        azure_service = AzureIntegrationService()
        
        if not azure_service.is_configured():
            return jsonify({'error': 'Azure services not configured'}), 503
        
        # Create streaming locator
        streaming_info = azure_service.create_streaming_locator(video_url)
        
        if not streaming_info:
            return jsonify({'error': 'Failed to create streaming endpoints'}), 500
        
        return jsonify({
            'original_url': video_url,
            'streaming': streaming_info
        })
        
    except Exception as e:
        current_app.logger.error(f"Error creating streaming endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@azure_bp.route('/analyze', methods=['POST'])
@cross_origin()
def analyze_video():
    """Analyze a video using Azure AI services."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        video_url = data.get('video_url', '')
        
        if not video_url:
            return jsonify({'error': 'Video URL is required'}), 400
        
        # Initialize Azure service
        azure_service = AzureIntegrationService()
        
        # Analyze video with AI
        analysis = azure_service.analyze_video_with_ai(video_url)
        
        if not analysis:
            return jsonify({'error': 'Failed to analyze video'}), 500
        
        return jsonify({
            'video_url': video_url,
            'analysis': analysis
        })
        
    except Exception as e:
        current_app.logger.error(f"Error analyzing video: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@azure_bp.route('/metrics/<video_id>', methods=['GET'])
@cross_origin()
def get_video_metrics(video_id):
    """Get analytics and metrics for a video."""
    try:
        # Initialize Azure service
        azure_service = AzureIntegrationService()
        
        # Get video metrics
        metrics = azure_service.get_video_metrics(video_id)
        
        if not metrics:
            return jsonify({'error': 'Failed to get video metrics'}), 500
        
        return jsonify({
            'video_id': video_id,
            'metrics': metrics
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting video metrics: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@azure_bp.route('/workflow', methods=['POST'])
@cross_origin()
def complete_azure_workflow():
    """Complete workflow: generate video, upload to Azure, create streaming endpoints."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        video_path = data.get('video_path', '')
        
        if not video_path or not os.path.exists(video_path):
            return jsonify({'error': 'Valid video path is required'}), 400
        
        # Initialize Azure service
        azure_service = AzureIntegrationService()
        
        if not azure_service.is_configured():
            return jsonify({'error': 'Azure services not configured'}), 503
        
        workflow_results = {}
        
        # Step 1: Upload to Azure Blob Storage
        blob_url = azure_service.upload_video_to_blob(video_path)
        if blob_url:
            workflow_results['upload'] = {
                'status': 'success',
                'blob_url': blob_url
            }
            
            # Step 2: Create CDN endpoint
            cdn_url = azure_service.create_cdn_endpoint(blob_url)
            if cdn_url:
                workflow_results['cdn'] = {
                    'status': 'success',
                    'cdn_url': cdn_url
                }
            
            # Step 3: Create streaming endpoints
            streaming_info = azure_service.create_streaming_locator(blob_url)
            if streaming_info:
                workflow_results['streaming'] = {
                    'status': 'success',
                    'endpoints': streaming_info
                }
            
            # Step 4: Analyze with AI (optional)
            analysis = azure_service.analyze_video_with_ai(blob_url)
            if analysis:
                workflow_results['analysis'] = {
                    'status': 'success',
                    'insights': analysis
                }
        else:
            workflow_results['upload'] = {
                'status': 'failed',
                'error': 'Failed to upload to Azure Blob Storage'
            }
        
        return jsonify({
            'original_path': video_path,
            'workflow': workflow_results,
            'status': 'completed'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in Azure workflow: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

