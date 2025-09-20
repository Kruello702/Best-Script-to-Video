import os
import tempfile
import subprocess
import time
import uuid
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class VideoGeneratorService:
    """Service for generating videos from scripts."""
    
    def __init__(self):
        self.output_dir = os.path.join(tempfile.gettempdir(), 'generated_videos')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Style configurations
        self.style_configs = {
            'real': {
                'description': 'photorealistic, cinematic, high quality, professional lighting, realistic textures',
                'keywords': ['cinematic', 'photorealistic', 'professional', 'high-definition']
            },
            'anime': {
                'description': 'anime style, vibrant colors, Japanese animation, detailed characters, cel-shaded',
                'keywords': ['anime', 'manga', 'Japanese animation', 'vibrant colors', 'stylized']
            },
            'cartoon': {
                'description': 'cartoon style, colorful, animated, family-friendly, stylized, 2D animation',
                'keywords': ['cartoon', 'animated', 'colorful', 'stylized', '2D']
            },
            'fantasy': {
                'description': 'fantasy style, magical, ethereal, mystical atmosphere, enchanted',
                'keywords': ['fantasy', 'magical', 'mystical', 'ethereal', 'enchanted']
            },
            'sci-fi': {
                'description': 'science fiction, futuristic, high-tech, cyberpunk, neon lights',
                'keywords': ['sci-fi', 'futuristic', 'cyberpunk', 'high-tech', 'neon']
            }
        }
    
    def generate_from_script(self, script: str, style: str = 'real', 
                           duration: int = 5, aspect_ratio: str = 'landscape',
                           video_id: str = None) -> Optional[str]:
        """
        Generate a video from a script using advanced AI video generation.
        
        Args:
            script: The input script/text
            style: Video style (real, anime, cartoon, fantasy, sci-fi)
            duration: Video duration in seconds
            aspect_ratio: Video aspect ratio (landscape, portrait, square)
            video_id: Unique identifier for the video
            
        Returns:
            Path to the generated video file, or None if generation failed
        """
        try:
            # Generate video ID if not provided
            if not video_id:
                video_id = str(uuid.uuid4())
            
            # Create detailed prompts for video generation
            prompts = self._create_scene_prompts(script, style, duration)
            
            # Generate video clips for each scene
            video_clips = []
            for i, prompt in enumerate(prompts):
                clip_path = self._generate_video_clip(
                    prompt, style, aspect_ratio, f"{video_id}_clip_{i}"
                )
                if clip_path:
                    video_clips.append(clip_path)
            
            if not video_clips:
                logger.error("No video clips were generated successfully")
                return None
            
            # Concatenate clips if multiple
            if len(video_clips) == 1:
                final_path = os.path.join(self.output_dir, f"{video_id}.mp4")
                os.rename(video_clips[0], final_path)
                return final_path
            else:
                return self._concatenate_clips(video_clips, video_id)
                
        except Exception as e:
            logger.error(f"Error in generate_from_script: {str(e)}")
            return None
    
    def _create_scene_prompts(self, script: str, style: str, duration: int) -> List[str]:
        """Break down script into scene prompts."""
        # For now, create a single comprehensive prompt
        # In a more advanced version, this could use NLP to break down the script
        style_config = self.style_configs.get(style, self.style_configs['real'])
        
        # Create a detailed prompt incorporating the script and style
        prompt = f"{script}. {style_config['description']}. High quality video production, smooth camera movement, professional cinematography."
        
        # For longer durations, we might want to create multiple scenes
        if duration > 10:
            # Split into multiple scenes for longer videos
            scenes = self._split_script_into_scenes(script, duration)
            prompts = []
            for scene in scenes:
                scene_prompt = f"{scene}. {style_config['description']}. High quality video production."
                prompts.append(scene_prompt)
            return prompts
        else:
            return [prompt]
    
    def _split_script_into_scenes(self, script: str, duration: int) -> List[str]:
        """Split script into multiple scenes for longer videos."""
        # Simple implementation: split by sentences
        sentences = script.split('. ')
        scenes_per_duration = max(1, len(sentences) // (duration // 5))  # ~5 seconds per scene
        
        scenes = []
        for i in range(0, len(sentences), scenes_per_duration):
            scene = '. '.join(sentences[i:i + scenes_per_duration])
            if scene:
                scenes.append(scene)
        
        return scenes if scenes else [script]
    
    def _generate_video_clip(self, prompt: str, style: str, aspect_ratio: str, clip_id: str) -> Optional[str]:
        """Generate a single video clip."""
        try:
            output_path = os.path.join(self.output_dir, f"{clip_id}.mp4")
            
            # Map aspect ratios
            aspect_map = {
                'landscape': 'landscape',
                'portrait': 'portrait', 
                'square': 'square'
            }
            
            mapped_aspect = aspect_map.get(aspect_ratio, 'landscape')
            
            # For now, use a placeholder implementation
            # In production, this would use the media_generate_video tool
            success = self._generate_placeholder_video(output_path, 5, prompt)
            
            return output_path if success else None
            
        except Exception as e:
            logger.error(f"Error generating video clip: {str(e)}")
            return None
    
    def _concatenate_clips(self, clip_paths: List[str], video_id: str) -> Optional[str]:
        """Concatenate multiple video clips into a single video."""
        try:
            output_path = os.path.join(self.output_dir, f"{video_id}.mp4")
            
            # Create a file list for ffmpeg
            list_file = os.path.join(self.output_dir, f"{video_id}_list.txt")
            with open(list_file, 'w') as f:
                for clip_path in clip_paths:
                    f.write(f"file '{clip_path}'\n")
            
            # Use ffmpeg to concatenate
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', list_file,
                '-c', 'copy',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Clean up temporary files
            os.remove(list_file)
            for clip_path in clip_paths:
                if os.path.exists(clip_path):
                    os.remove(clip_path)
            
            if result.returncode == 0 and os.path.exists(output_path):
                return output_path
            else:
                logger.error(f"FFmpeg concatenation error: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error concatenating clips: {str(e)}")
            return None
    
    def _generate_placeholder_video(self, output_path: str, duration: int, prompt: str) -> bool:
        """
        Generate a placeholder video using ffmpeg.
        This is a temporary implementation until we integrate proper video generation.
        """
        try:
            # Create a simple colored video with text overlay
            # Use different colors based on style
            colors = {
                'real': 'darkblue',
                'anime': 'purple', 
                'cartoon': 'orange',
                'fantasy': 'darkgreen',
                'sci-fi': 'darkred'
            }
            
            # Extract style from prompt (simple heuristic)
            color = 'darkblue'  # default
            for style, style_color in colors.items():
                if style in prompt.lower():
                    color = style_color
                    break
            
            cmd = [
                'ffmpeg', '-y',  # Overwrite output file
                '-f', 'lavfi',
                '-i', f'color=c={color}:size=1280x720:duration={duration}',
                '-vf', f'drawtext=text=\'{prompt[:100]}...\':fontcolor=white:fontsize=20:x=(w-text_w)/2:y=(h-text_h)/2:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"Successfully generated placeholder video: {output_path}")
                return True
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Video generation timed out")
            return False
        except Exception as e:
            logger.error(f"Error generating placeholder video: {str(e)}")
            return False
    
    def get_supported_styles(self) -> Dict[str, str]:
        """Get list of supported video styles."""
        return {
            'real': 'Photorealistic',
            'anime': 'Anime Style',
            'cartoon': 'Cartoon Style',
            'fantasy': 'Fantasy Style',
            'sci-fi': 'Science Fiction'
        }
    
    def get_supported_aspect_ratios(self) -> Dict[str, str]:
        """Get list of supported aspect ratios."""
        return {
            'landscape': '16:9 Landscape',
            'portrait': '9:16 Portrait', 
            'square': '1:1 Square'
        }
    
    def get_style_preview(self, style: str) -> Dict[str, Any]:
        """Get preview information for a style."""
        config = self.style_configs.get(style, self.style_configs['real'])
        return {
            'style': style,
            'description': config['description'],
            'keywords': config['keywords']
        }

