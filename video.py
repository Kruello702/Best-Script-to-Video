from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
import os
import uuid
import tempfile
from datetime import datetime
from src.services.video_generator import VideoGeneratorService

video_bp = Blueprint('video', __name__)

@video_bp.route('/generate', methods=['POST'])
@cross_origin()
def generate_video():
    """Generate a video from a script."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        script = data.get('script', '')
        style = data.get('style', 'real')
        duration = data.get('duration', 5)  # Default 5 seconds
        aspect_ratio = data.get('aspect_ratio', 'landscape')
        
        if not script:
            return jsonify({'error': 'Script is required'}), 400
        
        # Generate unique ID for this video
        video_id = str(uuid.uuid4())
        
        # Initialize video generator service
        generator = VideoGeneratorService()
        
        # Generate video
        video_path = generator.generate_from_script(
            script=script,
            style=style,
            duration=duration,
            aspect_ratio=aspect_ratio,
            video_id=video_id
        )
        
        if not video_path or not os.path.exists(video_path):
            return jsonify({'error': 'Failed to generate video'}), 500
        
        # Return video information
        return jsonify({
            'video_id': video_id,
            'video_path': video_path,
            'status': 'completed',
            'created_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        current_app.logger.error(f"Error generating video: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@video_bp.route('/status/<video_id>', methods=['GET'])
@cross_origin()
def get_video_status(video_id):
    """Get the status of a video generation task."""
    try:
        # For now, we'll assume all videos are completed immediately
        # In a real implementation, this would check a database or queue
        return jsonify({
            'video_id': video_id,
            'status': 'completed'
        })
    except Exception as e:
        current_app.logger.error(f"Error getting video status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@video_bp.route('/download/<video_id>', methods=['GET'])
@cross_origin()
def download_video(video_id):
    """Download a generated video."""
    try:
        # In a real implementation, this would serve the video file
        # For now, we'll return a placeholder response
        return jsonify({
            'video_id': video_id,
            'download_url': f'/api/video/file/{video_id}'
        })
    except Exception as e:
        current_app.logger.error(f"Error downloading video: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

