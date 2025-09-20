import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Scissors, Volume2, Type, Palette, Zap, Save, Undo, Redo } from 'lucide-react';

const VideoEditor = ({ videoPath, onSave }) => {
  const [editConfig, setEditConfig] = useState({});
  const [selectedPreset, setSelectedPreset] = useState('');
  const [isEditing, setIsEditing] = useState(false);

  const presets = {
    'social_media_short': {
      name: 'Social Media Short',
      description: 'Optimize for Instagram, TikTok (9:16, max 30s)',
      icon: '📱'
    },
    'youtube_intro': {
      name: 'YouTube Intro',
      description: 'YouTube video intro style (16:9)',
      icon: '🎬'
    },
    'cinematic': {
      name: 'Cinematic',
      description: 'Cinematic style with fades',
      icon: '🎭'
    },
    'fast_paced': {
      name: 'Fast Paced',
      description: 'Fast-paced action style',
      icon: '⚡'
    }
  };

  const updateEditConfig = (section, key, value) => {
    setEditConfig(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [key]: value
      }
    }));
  };

  const applyPreset = async (presetKey) => {
    try {
      const response = await fetch('/api/editor/presets');
      const data = await response.json();
      const preset = data.presets[presetKey];
      
      if (preset) {
        setEditConfig(preset.config);
        setSelectedPreset(presetKey);
      }
    } catch (error) {
      console.error('Error applying preset:', error);
    }
  };

  const saveEdits = async () => {
    if (!videoPath) {
      alert('No video selected for editing');
      return;
    }

    setIsEditing(true);

    try {
      const response = await fetch('/api/editor/edit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_path: videoPath,
          edit_config: editConfig,
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        onSave?.(data.edited_path);
        alert('Video edited successfully!');
      } else {
        throw new Error(data.error || 'Failed to edit video');
      }
    } catch (error) {
      console.error('Error editing video:', error);
      alert('Error editing video: ' + error.message);
    } finally {
      setIsEditing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold flex items-center justify-center space-x-2">
          <Scissors className="h-8 w-8 text-purple-600" />
          <span>Video Editor</span>
        </h2>
        <p className="text-gray-600">Fine-tune your generated video with professional editing tools</p>
      </div>

      {/* Quick Presets */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Presets</CardTitle>
          <CardDescription>Apply pre-configured editing styles</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(presets).map(([key, preset]) => (
              <Button
                key={key}
                variant={selectedPreset === key ? "default" : "outline"}
                className="h-auto p-4 flex flex-col items-center space-y-2"
                onClick={() => applyPreset(key)}
              >
                <span className="text-2xl">{preset.icon}</span>
                <div className="text-center">
                  <div className="font-medium">{preset.name}</div>
                  <div className="text-xs text-gray-500">{preset.description}</div>
                </div>
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Editing Controls */}
      <Tabs defaultValue="basic" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="basic">Basic</TabsTrigger>
          <TabsTrigger value="effects">Effects</TabsTrigger>
          <TabsTrigger value="text">Text</TabsTrigger>
          <TabsTrigger value="audio">Audio</TabsTrigger>
        </TabsList>

        {/* Basic Editing */}
        <TabsContent value="basic" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Scissors className="h-5 w-5" />
                <span>Basic Editing</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Trim Controls */}
              <div className="space-y-4">
                <Label className="text-base font-medium">Trim Video</Label>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="start-time">Start Time (seconds)</Label>
                    <Input
                      id="start-time"
                      type="number"
                      placeholder="0"
                      onChange={(e) => updateEditConfig('trim', 'start', parseFloat(e.target.value) || 0)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="end-time">End Time (seconds)</Label>
                    <Input
                      id="end-time"
                      type="number"
                      placeholder="Auto"
                      onChange={(e) => updateEditConfig('trim', 'end', parseFloat(e.target.value))}
                    />
                  </div>
                </div>
              </div>

              {/* Resize Controls */}
              <div className="space-y-4">
                <Label className="text-base font-medium">Resize Video</Label>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="width">Width (pixels)</Label>
                    <Input
                      id="width"
                      type="number"
                      placeholder="1920"
                      onChange={(e) => updateEditConfig('resize', 'width', parseInt(e.target.value))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="height">Height (pixels)</Label>
                    <Input
                      id="height"
                      type="number"
                      placeholder="1080"
                      onChange={(e) => updateEditConfig('resize', 'height', parseInt(e.target.value))}
                    />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Effects */}
        <TabsContent value="effects" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Palette className="h-5 w-5" />
                <span>Visual Effects</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Fade Effects */}
              <div className="space-y-4">
                <Label className="text-base font-medium">Fade Effects</Label>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="fade-in">Fade In Duration (seconds)</Label>
                    <Slider
                      defaultValue={[0]}
                      max={5}
                      step={0.1}
                      onValueChange={(value) => updateEditConfig('fade_in', 'duration', value[0])}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="fade-out">Fade Out Duration (seconds)</Label>
                    <Slider
                      defaultValue={[0]}
                      max={5}
                      step={0.1}
                      onValueChange={(value) => updateEditConfig('fade_out', 'duration', value[0])}
                    />
                  </div>
                </div>
              </div>

              {/* Visual Effects */}
              <div className="space-y-4">
                <Label className="text-base font-medium">Visual Effects</Label>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="bw-effect">Black & White</Label>
                    <Switch
                      id="bw-effect"
                      onCheckedChange={(checked) => {
                        if (checked) {
                          updateEditConfig('effects', 'list', ['black_and_white']);
                        }
                      }}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label htmlFor="speed-effect">Speed Up (2x)</Label>
                    <Switch
                      id="speed-effect"
                      onCheckedChange={(checked) => {
                        if (checked) {
                          updateEditConfig('effects', 'list', ['speed_up']);
                        }
                      }}
                    />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label htmlFor="slow-effect">Slow Motion (0.5x)</Label>
                    <Switch
                      id="slow-effect"
                      onCheckedChange={(checked) => {
                        if (checked) {
                          updateEditConfig('effects', 'list', ['slow_motion']);
                        }
                      }}
                    />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Text Overlays */}
        <TabsContent value="text" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Type className="h-5 w-5" />
                <span>Text Overlays</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="overlay-text">Text</Label>
                  <Input
                    id="overlay-text"
                    placeholder="Enter text to overlay"
                    onChange={(e) => updateEditConfig('text_overlays', 'text', e.target.value)}
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="font-size">Font Size</Label>
                    <Slider
                      defaultValue={[50]}
                      max={100}
                      min={20}
                      onValueChange={(value) => updateEditConfig('text_overlays', 'fontsize', value[0])}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="text-color">Text Color</Label>
                    <Select onValueChange={(value) => updateEditConfig('text_overlays', 'color', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select color" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="white">White</SelectItem>
                        <SelectItem value="black">Black</SelectItem>
                        <SelectItem value="red">Red</SelectItem>
                        <SelectItem value="blue">Blue</SelectItem>
                        <SelectItem value="yellow">Yellow</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="text-start">Start Time (s)</Label>
                    <Input
                      id="text-start"
                      type="number"
                      placeholder="0"
                      onChange={(e) => updateEditConfig('text_overlays', 'start', parseFloat(e.target.value) || 0)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="text-duration">Duration (s)</Label>
                    <Input
                      id="text-duration"
                      type="number"
                      placeholder="5"
                      onChange={(e) => updateEditConfig('text_overlays', 'duration', parseFloat(e.target.value) || 5)}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="text-position">Position</Label>
                    <Select onValueChange={(value) => updateEditConfig('text_overlays', 'position', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Position" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="center">Center</SelectItem>
                        <SelectItem value="top">Top</SelectItem>
                        <SelectItem value="bottom">Bottom</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Audio */}
        <TabsContent value="audio" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Volume2 className="h-5 w-5" />
                <span>Audio Settings</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <Label className="text-base font-medium">Volume Control</Label>
                <div className="space-y-2">
                  <Label htmlFor="volume-slider">Volume Factor</Label>
                  <Slider
                    defaultValue={[1]}
                    max={2}
                    min={0}
                    step={0.1}
                    onValueChange={(value) => updateEditConfig('volume', 'factor', value[0])}
                  />
                  <div className="text-sm text-gray-500">
                    Current: {editConfig.volume?.factor || 1}x
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Action Buttons */}
      <div className="flex justify-between items-center">
        <div className="flex space-x-2">
          <Button variant="outline" size="sm">
            <Undo className="h-4 w-4 mr-2" />
            Undo
          </Button>
          <Button variant="outline" size="sm">
            <Redo className="h-4 w-4 mr-2" />
            Redo
          </Button>
        </div>
        
        <div className="flex space-x-2">
          <Button variant="outline" onClick={() => setEditConfig({})}>
            Reset
          </Button>
          <Button onClick={saveEdits} disabled={isEditing || !videoPath}>
            {isEditing ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Processing...
              </>
            ) : (
              <>
                <Save className="h-4 w-4 mr-2" />
                Apply Edits
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Current Config Display */}
      {Object.keys(editConfig).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Current Configuration</CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="text-sm bg-gray-50 p-3 rounded overflow-auto">
              {JSON.stringify(editConfig, null, 2)}
            </pre>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default VideoEditor;

