from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
import os
from src.services.video_editor import VideoEditorService

editor_bp = Blueprint('editor', __name__)

@editor_bp.route('/edit', methods=['POST'])
@cross_origin()
def edit_video():
    """Edit a video with specified operations."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        video_path = data.get('video_path', '')
        edit_config = data.get('edit_config', {})
        
        if not video_path:
            return jsonify({'error': 'Video path is required'}), 400
        
        if not os.path.exists(video_path):
            return jsonify({'error': 'Video file not found'}), 404
        
        # Initialize video editor service
        editor = VideoEditorService()
        
        # Edit the video
        edited_video_path = editor.edit_video(video_path, edit_config)
        
        if not edited_video_path:
            return jsonify({'error': 'Failed to edit video'}), 500
        
        return jsonify({
            'original_path': video_path,
            'edited_path': edited_video_path,
            'status': 'completed'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error editing video: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@editor_bp.route('/concatenate', methods=['POST'])
@cross_origin()
def concatenate_videos():
    """Concatenate multiple videos into one."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        video_paths = data.get('video_paths', [])
        
        if len(video_paths) < 2:
            return jsonify({'error': 'At least 2 video paths are required'}), 400
        
        # Check if all files exist
        for path in video_paths:
            if not os.path.exists(path):
                return jsonify({'error': f'Video file not found: {path}'}), 404
        
        # Initialize video editor service
        editor = VideoEditorService()
        
        # Concatenate videos
        output_path = editor.concatenate_videos(video_paths)
        
        if not output_path:
            return jsonify({'error': 'Failed to concatenate videos'}), 500
        
        return jsonify({
            'input_paths': video_paths,
            'output_path': output_path,
            'status': 'completed'
        })
        
    except Exception as e:
        current_app.logger.error(f"Error concatenating videos: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@editor_bp.route('/info/<path:video_path>', methods=['GET'])
@cross_origin()
def get_video_info(video_path):
    """Get information about a video file."""
    try:
        if not os.path.exists(video_path):
            return jsonify({'error': 'Video file not found'}), 404
        
        # Initialize video editor service
        editor = VideoEditorService()
        
        # Get video info
        info = editor.get_video_info(video_path)
        
        if not info:
            return jsonify({'error': 'Failed to get video information'}), 500
        
        return jsonify({
            'video_path': video_path,
            'info': info
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting video info: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@editor_bp.route('/operations', methods=['GET'])
@cross_origin()
def get_supported_operations():
    """Get list of supported editing operations."""
    try:
        editor = VideoEditorService()
        operations = editor.get_supported_edits()
        
        return jsonify({'operations': operations})
        
    except Exception as e:
        current_app.logger.error(f"Error getting operations: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@editor_bp.route('/presets', methods=['GET'])
@cross_origin()
def get_editing_presets():
    """Get predefined editing presets."""
    presets = {
        'social_media_short': {
            'description': 'Optimize for social media (Instagram, TikTok)',
            'config': {
                'resize': {'width': 1080, 'height': 1920},  # 9:16 aspect ratio
                'trim': {'end': 30},  # Max 30 seconds
                'fade_in': {'duration': 0.5},
                'fade_out': {'duration': 0.5}
            }
        },
        'youtube_intro': {
            'description': 'YouTube video intro style',
            'config': {
                'resize': {'width': 1920, 'height': 1080},  # 16:9 aspect ratio
                'fade_in': {'duration': 1.0},
                'text_overlays': [{
                    'text': 'Welcome to my channel!',
                    'position': ('center', 'bottom'),
                    'start': 1,
                    'duration': 3,
                    'fontsize': 60,
                    'color': 'white'
                }]
            }
        },
        'cinematic': {
            'description': 'Cinematic style with fades',
            'config': {
                'fade_in': {'duration': 2.0},
                'fade_out': {'duration': 2.0},
                'effects': ['black_and_white']
            }
        },
        'fast_paced': {
            'description': 'Fast-paced action style',
            'config': {
                'effects': ['speed_up'],
                'volume': {'factor': 1.2}
            }
        }
    }
    
    return jsonify({'presets': presets})

