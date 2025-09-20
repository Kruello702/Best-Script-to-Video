import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Cloud, 
  Upload, 
  Play, 
  BarChart3, 
  Settings, 
  CheckCircle, 
  XCircle, 
  AlertCircle,
  Globe,
  Zap,
  Eye
} from 'lucide-react';

const AzureIntegration = ({ videoPath }) => {
  const [azureStatus, setAzureStatus] = useState(null);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [streamingInfo, setStreamingInfo] = useState(null);
  const [videoAnalysis, setVideoAnalysis] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    checkAzureStatus();
  }, []);

  const checkAzureStatus = async () => {
    try {
      const response = await fetch('/api/azure/status');
      const data = await response.json();
      setAzureStatus(data);
    } catch (error) {
      console.error('Error checking Azure status:', error);
    }
  };

  const uploadToAzure = async () => {
    if (!videoPath) {
      alert('No video selected for upload');
      return;
    }

    setIsUploading(true);

    try {
      const response = await fetch('/api/azure/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_path: videoPath,
          container_name: 'generated-videos'
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setUploadStatus(data);
        // Automatically create streaming endpoints
        createStreamingEndpoints(data.blob_url);
      } else {
        throw new Error(data.error || 'Failed to upload to Azure');
      }
    } catch (error) {
      console.error('Error uploading to Azure:', error);
      alert('Error uploading to Azure: ' + error.message);
    } finally {
      setIsUploading(false);
    }
  };

  const createStreamingEndpoints = async (videoUrl) => {
    try {
      const response = await fetch('/api/azure/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_url: videoUrl
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setStreamingInfo(data.streaming);
      }
    } catch (error) {
      console.error('Error creating streaming endpoints:', error);
    }
  };

  const analyzeVideo = async () => {
    if (!uploadStatus?.blob_url) {
      alert('Please upload video to Azure first');
      return;
    }

    setIsAnalyzing(true);

    try {
      const response = await fetch('/api/azure/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_url: uploadStatus.blob_url
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setVideoAnalysis(data.analysis);
      } else {
        throw new Error(data.error || 'Failed to analyze video');
      }
    } catch (error) {
      console.error('Error analyzing video:', error);
      alert('Error analyzing video: ' + error.message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const runCompleteWorkflow = async () => {
    if (!videoPath) {
      alert('No video selected');
      return;
    }

    setIsUploading(true);

    try {
      const response = await fetch('/api/azure/workflow', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_path: videoPath
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        const workflow = data.workflow;
        
        if (workflow.upload?.status === 'success') {
          setUploadStatus({
            blob_url: workflow.upload.blob_url,
            status: 'uploaded'
          });
        }
        
        if (workflow.streaming?.status === 'success') {
          setStreamingInfo(workflow.streaming.endpoints);
        }
        
        if (workflow.analysis?.status === 'success') {
          setVideoAnalysis(workflow.analysis.insights);
        }
      } else {
        throw new Error(data.error || 'Workflow failed');
      }
    } catch (error) {
      console.error('Error running workflow:', error);
      alert('Error running workflow: ' + error.message);
    } finally {
      setIsUploading(false);
    }
  };

  const StatusIcon = ({ status }) => {
    if (status === true) return <CheckCircle className="h-5 w-5 text-green-500" />;
    if (status === false) return <XCircle className="h-5 w-5 text-red-500" />;
    return <AlertCircle className="h-5 w-5 text-yellow-500" />;
  };

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold flex items-center justify-center space-x-2">
          <Cloud className="h-8 w-8 text-blue-600" />
          <span>Azure Integration</span>
        </h2>
        <p className="text-gray-600">Upload, stream, and analyze your videos with Microsoft Azure</p>
      </div>

      {/* Azure Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Settings className="h-5 w-5" />
            <span>Azure Configuration Status</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {azureStatus ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-center space-x-2">
                <StatusIcon status={azureStatus.services?.blob_storage} />
                <span>Blob Storage</span>
              </div>
              <div className="flex items-center space-x-2">
                <StatusIcon status={azureStatus.services?.media_services} />
                <span>Media Services</span>
              </div>
              <div className="flex items-center space-x-2">
                <StatusIcon status={azureStatus.services?.credentials_available} />
                <span>Credentials</span>
              </div>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-400"></div>
              <span>Checking Azure status...</span>
            </div>
          )}
          
          {azureStatus && !azureStatus.configured && (
            <Alert className="mt-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                Azure services are not fully configured. Please set up your Azure credentials and services.
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Main Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Button 
          onClick={uploadToAzure} 
          disabled={isUploading || !videoPath || !azureStatus?.configured}
          className="h-16 flex flex-col items-center space-y-1"
        >
          {isUploading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span className="text-sm">Uploading...</span>
            </>
          ) : (
            <>
              <Upload className="h-6 w-6" />
              <span>Upload to Azure</span>
            </>
          )}
        </Button>

        <Button 
          onClick={analyzeVideo} 
          disabled={isAnalyzing || !uploadStatus?.blob_url}
          variant="outline"
          className="h-16 flex flex-col items-center space-y-1"
        >
          {isAnalyzing ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-600"></div>
              <span className="text-sm">Analyzing...</span>
            </>
          ) : (
            <>
              <Eye className="h-6 w-6" />
              <span>Analyze Video</span>
            </>
          )}
        </Button>

        <Button 
          onClick={runCompleteWorkflow} 
          disabled={isUploading || !videoPath || !azureStatus?.configured}
          variant="secondary"
          className="h-16 flex flex-col items-center space-y-1"
        >
          <Zap className="h-6 w-6" />
          <span>Complete Workflow</span>
        </Button>
      </div>

      {/* Results Tabs */}
      <Tabs defaultValue="upload" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="upload">Upload & Streaming</TabsTrigger>
          <TabsTrigger value="analysis">AI Analysis</TabsTrigger>
          <TabsTrigger value="metrics">Metrics</TabsTrigger>
        </TabsList>

        {/* Upload & Streaming */}
        <TabsContent value="upload" className="space-y-4">
          {uploadStatus && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Upload className="h-5 w-5" />
                  <span>Upload Results</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center space-x-2">
                  <Badge variant="secondary">Status: {uploadStatus.status}</Badge>
                </div>
                
                <div className="space-y-2">
                  <p className="text-sm font-medium">Blob URL:</p>
                  <p className="text-sm text-gray-600 break-all">{uploadStatus.blob_url}</p>
                </div>
                
                {uploadStatus.cdn_url && (
                  <div className="space-y-2">
                    <p className="text-sm font-medium">CDN URL:</p>
                    <p className="text-sm text-gray-600 break-all">{uploadStatus.cdn_url}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {streamingInfo && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Play className="h-5 w-5" />
                  <span>Streaming Endpoints</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {streamingInfo.streaming_urls && (
                  <div className="space-y-3">
                    {Object.entries(streamingInfo.streaming_urls).map(([format, url]) => (
                      <div key={format} className="flex items-center justify-between">
                        <Badge variant="outline">{format.toUpperCase()}</Badge>
                        <Button variant="link" size="sm" className="text-blue-600">
                          <Globe className="h-4 w-4 mr-1" />
                          Stream
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* AI Analysis */}
        <TabsContent value="analysis" className="space-y-4">
          {videoAnalysis ? (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Eye className="h-5 w-5" />
                  <span>AI Video Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {videoAnalysis.insights && (
                  <div className="space-y-4">
                    {/* Keywords */}
                    {videoAnalysis.insights.keywords && (
                      <div>
                        <p className="font-medium mb-2">Keywords:</p>
                        <div className="flex flex-wrap gap-2">
                          {videoAnalysis.insights.keywords.map((keyword, index) => (
                            <Badge key={index} variant="secondary">{keyword}</Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Topics */}
                    {videoAnalysis.insights.topics && (
                      <div>
                        <p className="font-medium mb-2">Topics:</p>
                        <div className="flex flex-wrap gap-2">
                          {videoAnalysis.insights.topics.map((topic, index) => (
                            <Badge key={index} variant="outline">{topic}</Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Emotions */}
                    {videoAnalysis.insights.emotions && (
                      <div>
                        <p className="font-medium mb-2">Detected Emotions:</p>
                        <div className="flex flex-wrap gap-2">
                          {videoAnalysis.insights.emotions.map((emotion, index) => (
                            <Badge key={index} variant="default">{emotion}</Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Objects */}
                    {videoAnalysis.insights.objects && (
                      <div>
                        <p className="font-medium mb-2">Detected Objects:</p>
                        <div className="flex flex-wrap gap-2">
                          {videoAnalysis.insights.objects.map((object, index) => (
                            <Badge key={index} variant="secondary">{object}</Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Transcript */}
                    {videoAnalysis.insights.transcript && (
                      <div>
                        <p className="font-medium mb-2">Transcript:</p>
                        <p className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
                          {videoAnalysis.insights.transcript}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="text-center py-8">
                <Eye className="h-12 w-12 mx-auto text-gray-300 mb-4" />
                <p className="text-gray-500">No analysis results yet</p>
                <p className="text-sm text-gray-400">Upload a video and run analysis to see insights</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Metrics */}
        <TabsContent value="metrics" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5" />
                <span>Video Metrics</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <BarChart3 className="h-12 w-12 mx-auto text-gray-300 mb-4" />
                <p className="text-gray-500">Metrics will appear here</p>
                <p className="text-sm text-gray-400">Analytics data will be available after video deployment</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AzureIntegration;

