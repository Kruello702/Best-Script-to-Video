# Script to Video Generator

A comprehensive AI-powered application that transforms text scripts into stunning videos with multiple style options, professional editing capabilities, and Azure/Microsoft cloud integration.

## 🌟 Features

### Core Functionality
- **AI Video Generation**: Convert text scripts into videos using advanced AI models
- **Multiple Styles**: Choose from Real, Anime, Cartoon, Fantasy, and Sci-Fi styles
- **Customizable Settings**: Adjust duration, aspect ratio, and visual parameters
- **Real-time Progress**: Track video generation progress with live updates

### Professional Video Editing
- **Quick Presets**: Pre-configured editing styles for different platforms
  - Social Media Short (Instagram, TikTok)
  - YouTube Intro
  - Cinematic Style
  - Fast-Paced Action
- **Advanced Editing Tools**:
  - Trim and resize videos
  - Add visual effects (fade in/out, speed control)
  - Text overlays with customizable fonts and positioning
  - Audio volume control
- **Undo/Redo**: Full editing history management

### Azure/Microsoft Integration
- **Cloud Storage**: Upload videos to Azure Blob Storage
- **Global CDN**: Automatic CDN endpoint creation for fast worldwide delivery
- **Streaming Services**: Create HLS, DASH, and Smooth streaming endpoints
- **AI Analysis**: Leverage Azure AI Video Indexer for:
  - Automatic transcription
  - Keyword extraction
  - Emotion detection
  - Object recognition
  - Topic identification
- **Analytics**: Video performance metrics and viewer insights

## 🏗️ Architecture

### Backend (Flask)
```
script-to-video-backend/
├── src/
│   ├── main.py                 # Main Flask application
│   ├── routes/                 # API endpoints
│   │   ├── video.py           # Video generation endpoints
│   │   ├── editor.py          # Video editing endpoints
│   │   ├── styles.py          # Style management endpoints
│   │   └── azure.py           # Azure integration endpoints
│   ├── services/              # Business logic
│   │   ├── video_generator.py # Core video generation
│   │   ├── video_editor.py    # Video editing operations
│   │   └── azure_integration.py # Azure services
│   └── models/                # Data models
├── requirements.txt           # Python dependencies
└── venv/                     # Virtual environment
```

### Frontend (React)
```
script-to-video-frontend/
├── src/
│   ├── App.jsx               # Main application component
│   ├── components/           # React components
│   │   ├── VideoGenerator.jsx # Video generation interface
│   │   ├── VideoEditor.jsx   # Video editing interface
│   │   └── AzureIntegration.jsx # Azure features interface
│   └── components/ui/        # Reusable UI components
├── package.json              # Node.js dependencies
└── dist/                     # Built application
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 22+
- Azure account (optional, for cloud features)

### Backend Setup
```bash
cd script-to-video-backend
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

### Frontend Setup
```bash
cd script-to-video-frontend
pnpm install
pnpm run dev
```

### Access the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
# Azure Configuration (Optional)
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account
AZURE_STORAGE_ACCOUNT_KEY=your_storage_key
AZURE_MEDIA_SERVICES_ACCOUNT=your_media_account
AZURE_RESOURCE_GROUP=your_resource_group
AZURE_SUBSCRIPTION_ID=your_subscription_id

# OpenAI Configuration (for AI features)
OPENAI_API_KEY=your_openai_key
OPENAI_API_BASE=https://api.openai.com/v1
```

### Azure Services Setup
1. **Create Azure Storage Account**
   - Go to Azure Portal
   - Create a new Storage Account
   - Note the account name and access key

2. **Create Azure Media Services**
   - Create a new Media Services account
   - Link it to your storage account
   - Note the account details

3. **Configure Authentication**
   - Create a Service Principal or use Managed Identity
   - Grant appropriate permissions to your resources

## 📖 API Documentation

### Video Generation
```http
POST /api/video/generate
Content-Type: application/json

{
  "script": "A majestic dragon soaring through clouds",
  "style": "fantasy",
  "duration": 10,
  "aspect_ratio": "landscape"
}
```

### Video Editing
```http
POST /api/editor/edit
Content-Type: application/json

{
  "video_path": "/path/to/video.mp4",
  "edit_config": {
    "trim": {"start": 0, "end": 10},
    "resize": {"width": 1920, "height": 1080},
    "effects": {"list": ["fade_in"]},
    "text_overlays": {
      "text": "Hello World",
      "position": "center",
      "duration": 5
    }
  }
}
```

### Azure Integration
```http
POST /api/azure/upload
Content-Type: application/json

{
  "video_path": "/path/to/video.mp4",
  "container_name": "videos"
}
```

## 🎨 Supported Styles

| Style | Description | Best For |
|-------|-------------|----------|
| **Real** | Photorealistic videos | Professional content, documentaries |
| **Anime** | Japanese animation style | Entertainment, storytelling |
| **Cartoon** | Western cartoon style | Children's content, fun videos |
| **Fantasy** | Magical, mystical themes | Creative content, gaming |
| **Sci-Fi** | Futuristic, technological | Tech content, sci-fi stories |

## 🛠️ Development

### Adding New Styles
1. Update `src/services/video_generator.py`
2. Add style configuration in `get_available_styles()`
3. Update frontend style examples in `VideoGenerator.jsx`

### Adding New Editing Features
1. Extend `src/services/video_editor.py`
2. Add API endpoints in `src/routes/editor.py`
3. Update frontend UI in `VideoEditor.jsx`

### Extending Azure Integration
1. Add new methods to `src/services/azure_integration.py`
2. Create corresponding API endpoints
3. Update frontend Azure component

## 🔍 Troubleshooting

### Backend Issues
- **Server not starting**: Check Python version and dependencies
- **API not responding**: Verify Flask is listening on 0.0.0.0:5000
- **CORS errors**: Ensure Flask-CORS is properly configured

### Frontend Issues
- **Build errors**: Check Node.js version and run `pnpm install`
- **API connection**: Verify backend is running on port 5000
- **UI components**: Ensure all shadcn/ui components are properly imported

### Azure Issues
- **Authentication errors**: Verify Azure credentials and permissions
- **Upload failures**: Check storage account configuration
- **Streaming issues**: Ensure Media Services account is properly set up

## 📊 Performance Optimization

### Video Generation
- Use appropriate video resolution for target platform
- Optimize script length for faster processing
- Consider batch processing for multiple videos

### Editing Operations
- Process videos in chunks for large files
- Use hardware acceleration when available
- Cache intermediate results

### Azure Integration
- Use CDN for global content delivery
- Implement proper retry logic for API calls
- Monitor usage and costs

## 🔐 Security Considerations

- Store Azure credentials securely using environment variables
- Implement proper authentication for production deployment
- Validate all user inputs to prevent injection attacks
- Use HTTPS in production environments
- Regularly update dependencies to patch security vulnerabilities

## 📈 Scaling

### Horizontal Scaling
- Deploy multiple backend instances behind a load balancer
- Use Redis for session management and caching
- Implement queue system for video processing jobs

### Vertical Scaling
- Increase server resources for video processing
- Use GPU acceleration for AI operations
- Optimize database queries and indexing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation
- Contact the development team

## 🎯 Roadmap

### Short Term
- [ ] Fix backend connectivity issues
- [ ] Add real AI video generation integration
- [ ] Implement user authentication
- [ ] Add video preview functionality

### Medium Term
- [ ] Mobile app development
- [ ] Advanced AI features (voice synthesis, music generation)
- [ ] Collaboration features
- [ ] Template marketplace

### Long Term
- [ ] Multi-language support
- [ ] Enterprise features
- [ ] Advanced analytics dashboard
- [ ] API marketplace integration

---

**Built with ❤️ using Flask, React, and Azure**

