import os
import logging
from typing import Optional, Dict, Any
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.mgmt.media import AzureMediaServices
import requests
import json

logger = logging.getLogger(__name__)

class AzureIntegrationService:
    """Service for integrating with Azure Media Services and other Azure AI services."""
    
    def __init__(self):
        # Azure configuration - these would typically come from environment variables
        self.storage_account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
        self.storage_account_key = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
        self.media_services_account = os.getenv('AZURE_MEDIA_SERVICES_ACCOUNT')
        self.resource_group = os.getenv('AZURE_RESOURCE_GROUP')
        self.subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
        
        # Initialize clients if credentials are available
        self.blob_client = None
        self.media_client = None
        
        if self.storage_account_name and self.storage_account_key:
            try:
                self.blob_client = BlobServiceClient(
                    account_url=f"https://{self.storage_account_name}.blob.core.windows.net",
                    credential=self.storage_account_key
                )
            except Exception as e:
                logger.warning(f"Failed to initialize Azure Blob client: {str(e)}")
        
        if all([self.subscription_id, self.resource_group, self.media_services_account]):
            try:
                credential = DefaultAzureCredential()
                self.media_client = AzureMediaServices(
                    credential=credential,
                    subscription_id=self.subscription_id
                )
            except Exception as e:
                logger.warning(f"Failed to initialize Azure Media Services client: {str(e)}")
    
    def upload_video_to_blob(self, video_path: str, container_name: str = 'videos') -> Optional[str]:
        """
        Upload a video file to Azure Blob Storage.
        
        Args:
            video_path: Path to the video file to upload
            container_name: Name of the blob container
            
        Returns:
            URL of the uploaded blob, or None if upload failed
        """
        try:
            if not self.blob_client:
                logger.error("Azure Blob client not initialized")
                return None
            
            if not os.path.exists(video_path):
                logger.error(f"Video file not found: {video_path}")
                return None
            
            # Generate blob name
            filename = os.path.basename(video_path)
            blob_name = f"generated/{filename}"
            
            # Create container if it doesn't exist
            try:
                container_client = self.blob_client.get_container_client(container_name)
                container_client.create_container()
            except Exception:
                # Container might already exist
                pass
            
            # Upload the file
            with open(video_path, 'rb') as data:
                blob_client = self.blob_client.get_blob_client(
                    container=container_name,
                    blob=blob_name
                )
                blob_client.upload_blob(data, overwrite=True)
            
            # Return the blob URL
            blob_url = f"https://{self.storage_account_name}.blob.core.windows.net/{container_name}/{blob_name}"
            logger.info(f"Successfully uploaded video to Azure Blob: {blob_url}")
            return blob_url
            
        except Exception as e:
            logger.error(f"Error uploading video to Azure Blob: {str(e)}")
            return None
    
    def create_streaming_locator(self, video_url: str) -> Optional[Dict[str, Any]]:
        """
        Create a streaming locator for a video in Azure Media Services.
        
        Args:
            video_url: URL of the video in blob storage
            
        Returns:
            Dictionary with streaming URLs and metadata
        """
        try:
            if not self.media_client:
                logger.error("Azure Media Services client not initialized")
                return None
            
            # This is a simplified implementation
            # In a real scenario, you would need to:
            # 1. Create an asset
            # 2. Upload the video to the asset
            # 3. Create a transform and job for encoding
            # 4. Create a streaming locator
            # 5. Get streaming URLs
            
            # For now, return a mock response
            return {
                'streaming_urls': {
                    'hls': f"{video_url}?format=hls",
                    'dash': f"{video_url}?format=dash",
                    'smooth': f"{video_url}?format=smooth"
                },
                'status': 'ready'
            }
            
        except Exception as e:
            logger.error(f"Error creating streaming locator: {str(e)}")
            return None
    
    def analyze_video_with_ai(self, video_url: str) -> Optional[Dict[str, Any]]:
        """
        Analyze a video using Azure AI Video Indexer.
        
        Args:
            video_url: URL of the video to analyze
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # This would integrate with Azure AI Video Indexer
            # For now, return mock analysis results
            
            analysis_results = {
                'insights': {
                    'transcript': 'Mock transcript of the video content...',
                    'keywords': ['video', 'content', 'analysis'],
                    'faces': [],
                    'emotions': ['neutral', 'positive'],
                    'topics': ['technology', 'artificial intelligence'],
                    'brands': [],
                    'objects': ['computer', 'screen']
                },
                'thumbnails': [
                    {'time': '00:00:01', 'url': f"{video_url}_thumb_1.jpg"},
                    {'time': '00:00:05', 'url': f"{video_url}_thumb_2.jpg"}
                ],
                'status': 'completed'
            }
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error analyzing video with AI: {str(e)}")
            return None
    
    def get_video_metrics(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get analytics and metrics for a video.
        
        Args:
            video_id: Unique identifier for the video
            
        Returns:
            Dictionary with video metrics
        """
        try:
            # Mock metrics - in a real implementation, this would query Azure Analytics
            metrics = {
                'video_id': video_id,
                'views': 0,
                'play_time': '00:00:00',
                'completion_rate': 0.0,
                'geographic_distribution': {},
                'device_types': {},
                'quality_metrics': {
                    'average_bitrate': '1000 kbps',
                    'buffer_ratio': 0.02,
                    'startup_time': '2.1s'
                }
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting video metrics: {str(e)}")
            return None
    
    def create_cdn_endpoint(self, video_url: str) -> Optional[str]:
        """
        Create a CDN endpoint for global video delivery.
        
        Args:
            video_url: Original video URL
            
        Returns:
            CDN-enabled URL for faster global delivery
        """
        try:
            # Mock CDN URL - in a real implementation, this would create an Azure CDN endpoint
            cdn_url = video_url.replace('.blob.core.windows.net', '.azureedge.net')
            logger.info(f"Created CDN endpoint: {cdn_url}")
            return cdn_url
            
        except Exception as e:
            logger.error(f"Error creating CDN endpoint: {str(e)}")
            return None
    
    def is_configured(self) -> bool:
        """Check if Azure services are properly configured."""
        return bool(self.blob_client or self.media_client)
    
    def get_configuration_status(self) -> Dict[str, bool]:
        """Get the configuration status of various Azure services."""
        return {
            'blob_storage': bool(self.blob_client),
            'media_services': bool(self.media_client),
            'credentials_available': bool(
                self.storage_account_name and 
                self.storage_account_key and
                self.subscription_id
            )
        }
    
    def setup_instructions(self) -> Dict[str, Any]:
        """Get setup instructions for Azure integration."""
        return {
            'required_environment_variables': [
                'AZURE_STORAGE_ACCOUNT_NAME',
                'AZURE_STORAGE_ACCOUNT_KEY', 
                'AZURE_MEDIA_SERVICES_ACCOUNT',
                'AZURE_RESOURCE_GROUP',
                'AZURE_SUBSCRIPTION_ID'
            ],
            'azure_services_needed': [
                'Azure Storage Account',
                'Azure Media Services',
                'Azure AI Video Indexer (optional)',
                'Azure CDN (optional)'
            ],
            'setup_steps': [
                '1. Create an Azure Storage Account',
                '2. Create an Azure Media Services account',
                '3. Set up environment variables with account details',
                '4. Configure authentication (Service Principal or Managed Identity)',
                '5. Test the connection using the /api/azure/status endpoint'
            ]
        }

