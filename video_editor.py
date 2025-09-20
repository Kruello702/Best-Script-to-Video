import os
import tempfile
import time
import logging
from typing import Optional, Dict, Any, List
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
from moviepy.video.fx import resize, fadein, fadeout
from moviepy.audio.fx import volumex

logger = logging.getLogger(__name__)

class VideoEditorService:
    """Service for editing and enhancing generated videos."""
    
    def __init__(self):
        self.temp_dir = os.path.join(tempfile.gettempdir(), 'video_editing')
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def edit_video(self, video_path: str, edit_config: Dict[str, Any]) -> Optional[str]:
        """
        Apply editing operations to a video.
        
        Args:
            video_path: Path to the input video file
            edit_config: Dictionary containing editing instructions
            
        Returns:
            Path to the edited video file, or None if editing failed
        """
        try:
            if not os.path.exists(video_path):
                logger.error(f"Input video file not found: {video_path}")
                return None
            
            # Load the video
            video = VideoFileClip(video_path)
            
            # Apply editing operations
            edited_video = self._apply_edits(video, edit_config)
            
            if edited_video is None:
                logger.error("Failed to apply edits to video")
                return None
            
            # Generate output path
            output_filename = f"edited_{os.path.basename(video_path)}"
            output_path = os.path.join(self.temp_dir, output_filename)
            
            # Write the edited video
            edited_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            # Clean up
            video.close()
            edited_video.close()
            
            return output_path if os.path.exists(output_path) else None
            
        except Exception as e:
            logger.error(f"Error editing video: {str(e)}")
            return None
    
    def _apply_edits(self, video: VideoFileClip, edit_config: Dict[str, Any]) -> Optional[VideoFileClip]:
        """Apply individual editing operations to the video."""
        try:
            edited_video = video
            
            # Trim video if specified
            if 'trim' in edit_config:
                trim_config = edit_config['trim']
                start_time = trim_config.get('start', 0)
                end_time = trim_config.get('end', video.duration)
                edited_video = edited_video.subclip(start_time, end_time)
            
            # Resize video if specified
            if 'resize' in edit_config:
                resize_config = edit_config['resize']
                width = resize_config.get('width')
                height = resize_config.get('height')
                if width and height:
                    edited_video = edited_video.resize((width, height))
                elif 'scale' in resize_config:
                    scale = resize_config['scale']
                    edited_video = edited_video.resize(scale)
            
            # Add fade effects
            if 'fade_in' in edit_config:
                duration = edit_config['fade_in'].get('duration', 1.0)
                edited_video = edited_video.fx(fadein, duration)
            
            if 'fade_out' in edit_config:
                duration = edit_config['fade_out'].get('duration', 1.0)
                edited_video = edited_video.fx(fadeout, duration)
            
            # Adjust audio volume
            if 'volume' in edit_config:
                volume_factor = edit_config['volume'].get('factor', 1.0)
                if edited_video.audio:
                    edited_video = edited_video.fx(volumex, volume_factor)
            
            # Add text overlays
            if 'text_overlays' in edit_config:
                edited_video = self._add_text_overlays(edited_video, edit_config['text_overlays'])
            
            # Apply filters/effects
            if 'effects' in edit_config:
                edited_video = self._apply_effects(edited_video, edit_config['effects'])
            
            return edited_video
            
        except Exception as e:
            logger.error(f"Error applying edits: {str(e)}")
            return None
    
    def _add_text_overlays(self, video: VideoFileClip, text_configs: List[Dict[str, Any]]) -> VideoFileClip:
        """Add text overlays to the video."""
        try:
            clips = [video]
            
            for text_config in text_configs:
                text = text_config.get('text', '')
                if not text:
                    continue
                
                # Text properties
                fontsize = text_config.get('fontsize', 50)
                color = text_config.get('color', 'white')
                font = text_config.get('font', 'Arial')
                
                # Position and timing
                position = text_config.get('position', ('center', 'center'))
                start_time = text_config.get('start', 0)
                duration = text_config.get('duration', video.duration)
                
                # Create text clip
                text_clip = TextClip(
                    text,
                    fontsize=fontsize,
                    color=color,
                    font=font
                ).set_position(position).set_start(start_time).set_duration(duration)
                
                clips.append(text_clip)
            
            return CompositeVideoClip(clips)
            
        except Exception as e:
            logger.error(f"Error adding text overlays: {str(e)}")
            return video
    
    def _apply_effects(self, video: VideoFileClip, effects: List[str]) -> VideoFileClip:
        """Apply visual effects to the video."""
        try:
            edited_video = video
            
            for effect in effects:
                if effect == 'black_and_white':
                    # Convert to grayscale
                    edited_video = edited_video.fx(lambda clip: clip.fx(lambda frame: frame.mean(axis=2, keepdims=True).repeat(3, axis=2)))
                elif effect == 'speed_up':
                    # Speed up video by 2x
                    edited_video = edited_video.fx(lambda clip: clip.speedx(2))
                elif effect == 'slow_motion':
                    # Slow down video by 0.5x
                    edited_video = edited_video.fx(lambda clip: clip.speedx(0.5))
                # Add more effects as needed
            
            return edited_video
            
        except Exception as e:
            logger.error(f"Error applying effects: {str(e)}")
            return video
    
    def concatenate_videos(self, video_paths: List[str], output_path: str = None) -> Optional[str]:
        """Concatenate multiple videos into a single video."""
        try:
            if len(video_paths) < 2:
                logger.error("Need at least 2 videos to concatenate")
                return None
            
            # Load all video clips
            clips = []
            for path in video_paths:
                if os.path.exists(path):
                    clip = VideoFileClip(path)
                    clips.append(clip)
                else:
                    logger.warning(f"Video file not found: {path}")
            
            if not clips:
                logger.error("No valid video clips found")
                return None
            
            # Concatenate clips
            final_video = concatenate_videoclips(clips)
            
            # Generate output path if not provided
            if not output_path:
                output_path = os.path.join(self.temp_dir, f"concatenated_{int(time.time())}.mp4")
            
            # Write the final video
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            # Clean up
            for clip in clips:
                clip.close()
            final_video.close()
            
            return output_path if os.path.exists(output_path) else None
            
        except Exception as e:
            logger.error(f"Error concatenating videos: {str(e)}")
            return None
    
    def get_video_info(self, video_path: str) -> Optional[Dict[str, Any]]:
        """Get information about a video file."""
        try:
            if not os.path.exists(video_path):
                return None
            
            video = VideoFileClip(video_path)
            
            info = {
                'duration': video.duration,
                'fps': video.fps,
                'size': video.size,
                'width': video.w,
                'height': video.h,
                'has_audio': video.audio is not None
            }
            
            video.close()
            return info
            
        except Exception as e:
            logger.error(f"Error getting video info: {str(e)}")
            return None
    
    def get_supported_edits(self) -> Dict[str, Any]:
        """Get list of supported editing operations."""
        return {
            'trim': {
                'description': 'Trim video to specific start and end times',
                'parameters': ['start', 'end']
            },
            'resize': {
                'description': 'Resize video dimensions',
                'parameters': ['width', 'height', 'scale']
            },
            'fade_in': {
                'description': 'Add fade-in effect',
                'parameters': ['duration']
            },
            'fade_out': {
                'description': 'Add fade-out effect',
                'parameters': ['duration']
            },
            'volume': {
                'description': 'Adjust audio volume',
                'parameters': ['factor']
            },
            'text_overlays': {
                'description': 'Add text overlays to video',
                'parameters': ['text', 'position', 'start', 'duration', 'fontsize', 'color']
            },
            'effects': {
                'description': 'Apply visual effects',
                'options': ['black_and_white', 'speed_up', 'slow_motion']
            }
        }

