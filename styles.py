from flask import Blueprint, jsonify
from flask_cors import cross_origin
from src.services.video_generator import VideoGeneratorService

styles_bp = Blueprint('styles', __name__)

@styles_bp.route('/list', methods=['GET'])
@cross_origin()
def get_styles():
    """Get list of available video styles."""
    try:
        generator = VideoGeneratorService()
        styles = generator.get_supported_styles()
        aspect_ratios = generator.get_supported_aspect_ratios()
        
        return jsonify({
            'styles': styles,
            'aspect_ratios': aspect_ratios
        })
        
    except Exception as e:
        return jsonify({'error': 'Failed to get styles'}), 500

@styles_bp.route('/preview/<style>', methods=['GET'])
@cross_origin()
def get_style_preview(style):
    """Get preview information for a specific style."""
    try:
        generator = VideoGeneratorService()
        preview = generator.get_style_preview(style)
        
        return jsonify(preview)
        
    except Exception as e:
        return jsonify({'error': 'Failed to get style preview'}), 500

@styles_bp.route('/examples', methods=['GET'])
@cross_origin()
def get_style_examples():
    """Get example prompts for different styles."""
    examples = {
        'real': [
            "A serene mountain landscape at sunrise with mist rolling over the peaks",
            "A bustling city street at night with neon lights reflecting on wet pavement",
            "A close-up of ocean waves crashing against rocky cliffs"
        ],
        'anime': [
            "A magical girl transformation sequence with sparkles and flowing ribbons",
            "A samurai warrior standing in a cherry blossom garden",
            "A futuristic mecha robot flying through a cyberpunk cityscape"
        ],
        'cartoon': [
            "A friendly dragon playing with children in a colorful meadow",
            "A superhero cat saving the day in a comic book style city",
            "A group of animals having a tea party in an enchanted forest"
        ],
        'fantasy': [
            "A wizard casting spells in an ancient magical library",
            "Unicorns galloping through an enchanted forest with glowing flowers",
            "A dragon's lair filled with treasure and mystical artifacts"
        ],
        'sci-fi': [
            "A spaceship traveling through a wormhole with swirling galaxies",
            "Robots working in a futuristic factory with holographic displays",
            "An alien planet with floating cities and multiple moons"
        ]
    }
    
    return jsonify({'examples': examples})

