import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import VideoGenerator from './components/VideoGenerator';
import VideoEditor from './components/VideoEditor';
import AzureIntegration from './components/AzureIntegration';
import './App.css';

function App() {
  const [currentVideoPath, setCurrentVideoPath] = useState(null);

  const handleVideoGenerated = (videoData) => {
    setCurrentVideoPath(videoData.video_path);
  };

  const handleVideoEdited = (editedVideoPath) => {
    setCurrentVideoPath(editedVideoPath);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="container mx-auto py-8">
        <Tabs defaultValue="generate" className="w-full">
          <TabsList className="grid w-full grid-cols-3 mb-8">
            <TabsTrigger value="generate" className="text-lg py-3">
              Generate Video
            </TabsTrigger>
            <TabsTrigger value="edit" className="text-lg py-3">
              Edit Video
            </TabsTrigger>
            <TabsTrigger value="azure" className="text-lg py-3">
              Azure Integration
            </TabsTrigger>
          </TabsList>

          <TabsContent value="generate">
            <VideoGenerator onVideoGenerated={handleVideoGenerated} />
          </TabsContent>

          <TabsContent value="edit">
            <VideoEditor 
              videoPath={currentVideoPath} 
              onSave={handleVideoEdited}
            />
          </TabsContent>

          <TabsContent value="azure">
            <AzureIntegration videoPath={currentVideoPath} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

export default App;
