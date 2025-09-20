import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Play, Download, Edit, Upload, Sparkles, Video, Wand2 } from 'lucide-react';

const VideoGenerator = () => {
  const [script, setScript] = useState('');
  const [selectedStyle, setSelectedStyle] = useState('real');
  const [duration, setDuration] = useState([5]);
  const [aspectRatio, setAspectRatio] = useState('landscape');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedVideo, setGeneratedVideo] = useState(null);
  const [styles, setStyles] = useState({});
  const [progress, setProgress] = useState(0);

  // Fetch available styles on component mount
  useEffect(() => {
    fetchStyles();
  }, []);

  const fetchStyles = async () => {
    try {
      const response = await fetch('/api/styles/list');
      const data = await response.json();
      setStyles(data.styles || {});
    } catch (error) {
      console.error('Error fetching styles:', error);
    }
  };

  const generateVideo = async () => {
    if (!script.trim()) {
      alert('Please enter a script');
      return;
    }

    setIsGenerating(true);
    setProgress(0);

    // Simulate progress updates
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + Math.random() * 10;
      });
    }, 500);

    try {
      const response = await fetch('/api/video/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          script,
          style: selectedStyle,
          duration: duration[0],
          aspect_ratio: aspectRatio,
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setGeneratedVideo(data);
        setProgress(100);
      } else {
        throw new Error(data.error || 'Failed to generate video');
      }
    } catch (error) {
      console.error('Error generating video:', error);
      alert('Error generating video: ' + error.message);
    } finally {
      clearInterval(progressInterval);
      setIsGenerating(false);
    }
  };

  const styleExamples = {
    real: "A serene mountain landscape at sunrise with mist rolling over the peaks",
    anime: "A magical girl transformation sequence with sparkles and flowing ribbons",
    cartoon: "A friendly dragon playing with children in a colorful meadow",
    fantasy: "A wizard casting spells in an ancient magical library",
    'sci-fi': "A spaceship traveling through a wormhole with swirling galaxies"
  };

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center space-x-2">
          <Video className="h-8 w-8 text-blue-600" />
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Script to Video Generator
          </h1>
        </div>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Transform your scripts into stunning videos with AI-powered generation, multiple styles, and professional editing tools.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Panel */}
        <Card className="h-fit">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Wand2 className="h-5 w-5" />
              <span>Create Your Video</span>
            </CardTitle>
            <CardDescription>
              Enter your script and customize the video settings
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Script Input */}
            <div className="space-y-2">
              <Label htmlFor="script">Script</Label>
              <Textarea
                id="script"
                placeholder="Enter your video script here... Be descriptive and creative!"
                value={script}
                onChange={(e) => setScript(e.target.value)}
                className="min-h-32 resize-none"
              />
              <div className="text-sm text-gray-500">
                {script.length}/1000 characters
              </div>
            </div>

            {/* Style Selection */}
            <div className="space-y-2">
              <Label>Video Style</Label>
              <Select value={selectedStyle} onValueChange={setSelectedStyle}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a style" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(styles).map(([key, value]) => (
                    <SelectItem key={key} value={key}>
                      <div className="flex items-center space-x-2">
                        <Sparkles className="h-4 w-4" />
                        <span>{value}</span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {selectedStyle && styleExamples[selectedStyle] && (
                <div className="p-3 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">
                    <strong>Example:</strong> {styleExamples[selectedStyle]}
                  </p>
                </div>
              )}
            </div>

            {/* Duration Slider */}
            <div className="space-y-2">
              <Label>Duration: {duration[0]} seconds</Label>
              <Slider
                value={duration}
                onValueChange={setDuration}
                max={30}
                min={3}
                step={1}
                className="w-full"
              />
            </div>

            {/* Aspect Ratio */}
            <div className="space-y-2">
              <Label>Aspect Ratio</Label>
              <Select value={aspectRatio} onValueChange={setAspectRatio}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="landscape">16:9 Landscape</SelectItem>
                  <SelectItem value="portrait">9:16 Portrait</SelectItem>
                  <SelectItem value="square">1:1 Square</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Generate Button */}
            <Button 
              onClick={generateVideo} 
              disabled={isGenerating || !script.trim()}
              className="w-full h-12 text-lg"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Generating Video...
                </>
              ) : (
                <>
                  <Play className="h-5 w-5 mr-2" />
                  Generate Video
                </>
              )}
            </Button>

            {/* Progress Bar */}
            {isGenerating && (
              <div className="space-y-2">
                <Progress value={progress} className="w-full" />
                <p className="text-sm text-center text-gray-600">
                  {progress < 30 ? 'Processing script...' :
                   progress < 60 ? 'Generating video...' :
                   progress < 90 ? 'Applying style...' : 'Finalizing...'}
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Preview Panel */}
        <Card className="h-fit">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Video className="h-5 w-5" />
              <span>Video Preview</span>
            </CardTitle>
            <CardDescription>
              Your generated video will appear here
            </CardDescription>
          </CardHeader>
          <CardContent>
            {generatedVideo ? (
              <div className="space-y-4">
                {/* Video Player Placeholder */}
                <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center">
                  <div className="text-center space-y-2">
                    <Video className="h-12 w-12 mx-auto text-gray-400" />
                    <p className="text-gray-600">Video generated successfully!</p>
                    <Badge variant="secondary">
                      ID: {generatedVideo.video_id?.slice(0, 8)}...
                    </Badge>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex space-x-2">
                  <Button variant="outline" className="flex-1">
                    <Play className="h-4 w-4 mr-2" />
                    Play
                  </Button>
                  <Button variant="outline" className="flex-1">
                    <Download className="h-4 w-4 mr-2" />
                    Download
                  </Button>
                  <Button variant="outline" className="flex-1">
                    <Edit className="h-4 w-4 mr-2" />
                    Edit
                  </Button>
                  <Button variant="outline" className="flex-1">
                    <Upload className="h-4 w-4 mr-2" />
                    Upload to Azure
                  </Button>
                </div>

                {/* Video Info */}
                <div className="p-3 bg-gray-50 rounded-lg space-y-1">
                  <p className="text-sm"><strong>Status:</strong> {generatedVideo.status}</p>
                  <p className="text-sm"><strong>Created:</strong> {new Date(generatedVideo.created_at).toLocaleString()}</p>
                  <p className="text-sm"><strong>Style:</strong> {styles[selectedStyle]}</p>
                  <p className="text-sm"><strong>Duration:</strong> {duration[0]} seconds</p>
                </div>
              </div>
            ) : (
              <div className="aspect-video bg-gray-50 rounded-lg flex items-center justify-center">
                <div className="text-center space-y-2">
                  <Video className="h-12 w-12 mx-auto text-gray-300" />
                  <p className="text-gray-500">No video generated yet</p>
                  <p className="text-sm text-gray-400">Enter a script and click generate to create your video</p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default VideoGenerator;

