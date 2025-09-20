# Application Architecture

This document outlines the architecture for the script-to-video generator.

## Components

The application will consist of the following components:

*   **Frontend:** A web-based user interface for users to input scripts, select styles, and edit videos.
*   **Backend:** A server-side application that handles the core logic of the application, including:
    *   Script processing
    *   Video generation
    *   Video editing
    *   Integration with Azure services
*   **Video Generation Engine:** The core component responsible for generating videos from scripts. We will use **Open-Sora** for this.
*   **Video Editing Engine:** The component responsible for editing and enhancing videos. We will use the **MoviePy** library for this.
*   **Cloud Services:** We will use **Azure Media Services** for video hosting and streaming.

## Workflow

1.  The user enters a script and selects a style in the frontend.
2.  The frontend sends the script and style to the backend.
3.  The backend processes the script and uses the Open-Sora engine to generate a video.
4.  The backend uses the MoviePy library to apply any requested edits or enhancements.
5.  The backend uploads the final video to Azure Media Services.
6.  The backend returns the video URL to the frontend.
7.  The frontend displays the video to the user.


