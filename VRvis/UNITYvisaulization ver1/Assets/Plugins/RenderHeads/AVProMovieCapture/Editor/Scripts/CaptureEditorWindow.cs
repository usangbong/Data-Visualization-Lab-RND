﻿#if UNITY_EDITOR
#if UNITY_5_4_OR_NEWER || (UNITY_5 && !UNITY_5_0)
	#define AVPRO_MOVIECAPTURE_WINDOWTITLE_51
	#define AVPRO_MOVIECAPTURE_GRAPHICSDEVICETYPE_51
#endif
#if UNITY_5_4_OR_NEWER || (UNITY_5 && !UNITY_5_0 && !UNITY_5_1 && !UNITY_5_2)
	#define AVPRO_MOVIECAPTURE_SCENEMANAGER_53
#endif
#if UNITY_5_4_OR_NEWER || UNITY_5
	#define AVPRO_MOVIECAPTURE_DEFERREDSHADING
#endif
#if UNITY_2017_1_OR_NEWER
	#define AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
#endif
#if UNITY_2018_1_OR_NEWER
	// Unity 2018.1 introduces stereo cubemap render methods
	#define AVPRO_MOVIECAPTURE_UNITY_STEREOCUBEMAP_RENDER
#endif

using UnityEngine;
using UnityEditor;

//-----------------------------------------------------------------------------
// Copyright 2012-2019 RenderHeads Ltd.  All rights reserved.
//-----------------------------------------------------------------------------

namespace RenderHeads.Media.AVProMovieCapture.Editor
{
	/// <summary>
	/// Creates a dockable window in Unity that can be used for handy in-editor capturing
	/// </summary>
	public class CaptureEditorWindow : EditorWindow
	{
		private const string TempGameObjectName = "Temp97435_MovieCapture";
		private const string SettingsPrefix = "AVProMovieCapture.EditorWindow.";
		private const string SelectorPrefix = SettingsPrefix + "CameraSelector.";

		private GameObject _gameObject;
		private CaptureBase _capture;
		private CaptureFromScreen _captureScreen;
		private CaptureFromCamera _captureCamera;
		private CaptureFromCamera360 _captureCamera360;
		private CaptureFromCamera360ODS _captureCamera360ODS;
		private CameraSelector _cameraSelector;
#if AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
		private TimelineController _timelineController;
#endif

		private static bool _isTrialVersion = false;
		private static bool _isCreated = false;
		private static bool _isInit = false;
		private static bool _isFailedInit = false;
		private static bool _showAlpha = false;
		private static string[] _fileExtensions = new string[0];
		private static string[] _videoCodecNames = new string[0];
		private static string[] _audioCodecNames = new string[0];
		private static string[] _audioDeviceNames = new string[0];
		private static bool[] _videoCodecConfigurable = new bool[0];
		private static bool[] _audioCodecConfigurable = new bool[0];

		private readonly string[] _downScales = { "Original", "Half", "Quarter", "Eighth", "Sixteenth", "Custom" };
		private readonly string[] _captureModes = { "Realtime Capture", "Offline Render" };
		private readonly string[] _outputFolders = { "Project Folder", "Persistent Data Folder", "Absolute Folder", "Desktop" };
		private readonly string[] _sourceNames = { "Screen", "Camera", "Camera 360 (Mono+Stereo)", "Camera 360 (experimental ODS Stereo)" };
		private readonly string[] _tabNames = { "Capture", "Visual", "Audio", "Encoding" };

		private readonly static GUIContent _guiCameraSelectorTag = new GUIContent("Tag");
		private readonly static GUIContent _guiCameraSelectorName = new GUIContent("Name");
		private readonly static GUIContent _guiContributingCameras = new GUIContent("Contributing Cameras");
		private readonly static GUIContent _guiCaptureWorldSpaceUI= new GUIContent("Capture Worldspace UI");
		private readonly static GUIContent _guiCameraRotation = new GUIContent("Camera Rotation");
		private readonly static GUIContent _guiInterpupillaryDistance = new GUIContent("Interpupillary distance");
		private readonly static GUIContent _guiStartDelay = new GUIContent("Start Delay");
		private readonly static GUIContent _guiSeconds = new GUIContent("Seconds");
#if UNITY_EDITOR_WIN
		private readonly static GUIContent _guiStreamableMP4 = new GUIContent("Streamable MP4");
#endif
		private readonly static GUIContent _guiStartFrame = new GUIContent("Start Frame");
		private readonly static GUIContent _guiZeroDigits = new GUIContent("Zero Digits");

		private enum SourceType
		{
			Screen,
			Camera,
			Camera360,
			Camera360ODS,
		}

		private enum ConfigTabs
		{
			Capture = 0,
			Visual = 1,
			Audio = 2,
			Encoding = 3,
		}

		[SerializeField]
		private SourceType _sourceType = SourceType.Screen;

		private Camera _cameraNode;
		private string _cameraName;
		private int _captureModeIndex;
		private int _outputFolderIndex;

		[SerializeField]
		private CaptureBase.OutputType _outputType = CaptureBase.OutputType.VideoFile;
		[SerializeField]
		private ImageSequenceFormat _imageSequenceFormat = ImageSequenceFormat.PNG;
		private bool _filenamePrefixFromSceneName = true;
		private string _filenamePrefix = "capture";
#if UNITY_EDITOR_WIN
		private string _filenameExtension = "avi";
#else
		private string _filenameExtension = "mp4";
#endif
		private int _fileContainerIndex = 0;

		[SerializeField]
		private int _imageSequenceStartFrame = 0;
		[SerializeField]
		[Range(2, 12)]
		private int _imageSequenceZeroDigits = 6;
		private string _outputFolderRelative = "Captures";
		private string _outputFolderAbsolute = string.Empty;
		private bool _appendTimestamp = true;

		[SerializeField]
		private string _namedPipePath = @"\\.\pipe\pipename";

		private int _downScaleIndex;
		private int _downscaleX;
		private int _downscaleY;

		private bool _captureMouseCursor = false;
		private Texture2D _mouseCursorTexture = null;

		[SerializeField]
		private CaptureBase.Resolution _renderResolution = CaptureBase.Resolution.Original;
		private Vector2 _renderSize;

		[SerializeField]
		private int _renderAntiAliasing;

		[SerializeField]
		private bool _useContributingCameras = true;

		[SerializeField]
		private float _frameRate = 30f;

		[SerializeField]
		private int _timelapseScale = 1;

		private bool _supportAlpha = false;
		private bool _useMediaFoundationH264 = true;
		private int _videoCodecIndex;
		private bool _captureAudio;
		private int _audioCodecIndex;
		private int _audioDeviceIndex;
		private Vector2 _scroll = Vector2.zero;
		private bool _queueStart;
		private int _queueConfigureVideoCodec = -1;
		private int _queueConfigureAudioCodec = -1;

		private bool _useMotionBlur = false;
		private int _motionBlurSampleCount = 16;

		private int _cubemapResolution = 2048;
		private int _cubemapDepth = 24;
		[SerializeField]
		private bool _render180Degrees = false;
		[SerializeField]
		private bool _captureWorldSpaceGUI = false;
		[SerializeField]
		private bool _supportCameraRotation = false;
		[SerializeField]
		private bool _onlyLeftRightRotation = false;
		private int _cubemapStereoPacking = 0;
		private float _cubemapStereoIPD = 0.064f;

		[SerializeField]
		private StartDelayMode _startDelay = StartDelayMode.None;
		[SerializeField]
		private float _startDelaySeconds = 0f;

		[SerializeField]
		private StopMode _stopMode = StopMode.None;
		private int _stopFrames = 300;
		private float _stopSeconds = 10f;

		[SerializeField] CameraSelector.SelectByMode _selectBy = CameraSelector.SelectByMode.HighestDepthCamera;
		[SerializeField] CameraSelector.ScanFrequencyMode _scanFrequency = CameraSelector.ScanFrequencyMode.SceneLoad;
		[SerializeField] bool _scanHiddenCameras = false;
		[SerializeField] string _selectCameraTag = "MainCamera";
		[SerializeField] string _selectCameraName = "Main Camera";

		private SerializedProperty _propCameraSelectorSelectBy;
		private SerializedProperty _propCameraSelectorScanFrequency;
		private SerializedProperty _propCameraSelectorScanHiddenCameras;
		private SerializedProperty _propCameraSelectorTag;
		private SerializedProperty _propCameraSelectorName;

		private SerializedProperty _propSourceType;
		private SerializedProperty _propOutputType;
		private SerializedProperty _propImageSequenceFormat;
		private SerializedProperty _propImageSequenceStartFrame;
		private SerializedProperty _propImageSequenceZeroDigits;
		private SerializedProperty _propNamedPipePath;
		private SerializedProperty _propFrameRate;
		[Tooltip("Timelapse scale makes the frame capture run at a fraction of the target frame rate.  Default value is 1")]
		private SerializedProperty _propTimelapseScale;
		private SerializedProperty _propStartDelay;
		private SerializedProperty _propStartDelaySeconds;
		private SerializedProperty _propStopMode;
		private SerializedProperty _propRenderResolution;
		private SerializedProperty _propUseContributingCameras;
		private SerializedProperty _propRender180Degrees;
		private SerializedProperty _propCaptureWorldSpaceGUI;
		private SerializedProperty _propSupportCameraRotation;
		private SerializedProperty _propOnlyLeftRightRotation;

		private SerializedProperty _propRenderAntiAliasing;
		private SerializedProperty _propOdsRender180Degrees;
		private SerializedProperty _propOdsCamera;
		private SerializedProperty _propOdsIPD;
		private SerializedProperty _propOdsPixelSliceSize;
		private SerializedProperty _propOdsPaddingSize;
		private SerializedProperty _propOdsCameraClearMode;
		private SerializedProperty _propOdsCameraClearColor;

		[SerializeField]
		private CaptureFromCamera360ODS.Settings _odsSettings = new CaptureFromCamera360ODS.Settings();

#if UNITY_EDITOR_WIN
		private SerializedProperty _propPostFastStartMp4;
#endif
		[SerializeField]
		private CaptureBase.PostCaptureSettings _postCaptureSettings = new CaptureBase.PostCaptureSettings();

		// TODO: we should actually be saving these parameters per-scene...

		private long _lastFileSize;
		private uint _lastEncodedMinutes;
		private uint _lastEncodedSeconds;
		private uint _lastEncodedFrame;
		private int _selectedTool;
		private int _selectedConfigTab;
		private bool _expandSectionTrial = true;

		private static Texture2D _icon;
		private string _pluginVersionWarningText = string.Empty;

		private SerializedObject _so;

		private const string LinkPluginWebsite = "http://renderheads.com/product/av-pro-movie-capture/";
		private const string LinkForumPage = "http://forum.unity3d.com/threads/released-avpro-movie-capture.120717/";
		private const string LinkAssetStorePage = "https://www.assetstore.unity3d.com/#!/content/2670";
		private const string LinkFreeAssetStorePage = "https://www.assetstore.unity3d.com/#!/content/97562";
		private const string LinkSupport = "https://github.com/RenderHeads/UnityPlugin-AVProMovieCapture/issues";
		private const string LinkUserManual = "http://downloads.renderheads.com/docs/UnityAVProMovieCapture.pdf";

		private const string SupportMessage = "If you are reporting a bug, please include any relevant files and details so that we may remedy the problem as fast as possible.\n\n" +
			"Essential details:\n" +
			"+ Error message\n" +
			"      + The exact error message\n" +
			"      + The console/output log if possible\n" +
			"+ Development environment\n" +
			"      + Unity version\n" +
			"      + Development OS version\n" +
			"      + AVPro Movie Capture plugin version\n";

		[MenuItem("Window/Open AVPro Movie Capture..")]
		public static void Init()
		{
			if (_isInit || _isCreated)
			{
				CaptureEditorWindow window = (CaptureEditorWindow)EditorWindow.GetWindow(typeof(CaptureEditorWindow));
				window.Close();
				return;
			}

			_isCreated = true;

			// Get existing open window or if none, make a new one:
			CaptureEditorWindow window2 = (CaptureEditorWindow)EditorWindow.GetWindow(typeof(CaptureEditorWindow));
			if (window2 != null)
			{
				window2.SetupWindow();
			}
		}

		public void SetupWindow()
		{
			_isCreated = true;
			if ((Application.platform == RuntimePlatform.WindowsEditor)
			||  (Application.platform == RuntimePlatform.OSXEditor))
			{
				this.minSize = new Vector2(200f, 48f);
				this.maxSize = new Vector2(340f, 620f);
#if AVPRO_MOVIECAPTURE_WINDOWTITLE_51
				if (_icon != null)
				{
					this.titleContent = new GUIContent("Movie Capture", _icon, "AVPro Movie Capture");
				}
				else
				{
					this.titleContent = new GUIContent("Movie Capture", "AVPro Movie Capture");
				}
#else
				this.title = "Movie Capture";
#endif
				this.CreateGUI();
				this.LoadSettings();

				_so = new SerializedObject(this);
				if (_so == null)
				{
					Debug.LogError("[AVProMovieCapture] SO is null");
				}

				_propSourceType = _so.FindProperty("_sourceType");
				_propOutputType = _so.FindProperty("_outputType");
				_propImageSequenceFormat = _so.FindProperty("_imageSequenceFormat");
				_propImageSequenceStartFrame = _so.FindProperty("_imageSequenceStartFrame");
				_propImageSequenceZeroDigits = _so.FindProperty("_imageSequenceZeroDigits");
				_propNamedPipePath = _so.FindProperty("_namedPipePath");
				_propRenderResolution = _so.FindProperty("_renderResolution");
				_propUseContributingCameras = _so.FindProperty("_useContributingCameras");
				_propRender180Degrees = _so.FindProperty("_render180Degrees");
				_propCaptureWorldSpaceGUI = _so.FindProperty("_captureWorldSpaceGUI");
				_propSupportCameraRotation = _so.FindProperty("_supportCameraRotation");
				_propOnlyLeftRightRotation = _so.FindProperty("_onlyLeftRightRotation");

				_propFrameRate = _so.FindProperty("_frameRate");
				_propTimelapseScale = _so.FindProperty("_timelapseScale");

				// Start/Stop
				_propStopMode = _so.FindProperty("_stopMode");
				_propStartDelay = _so.FindProperty("_startDelay");
				_propStartDelaySeconds = _so.FindProperty("_startDelaySeconds");

				// Camera Selector
				_propCameraSelectorSelectBy = _so.FindProperty("_selectBy");
				_propCameraSelectorScanFrequency = _so.FindProperty("_scanFrequency");
				_propCameraSelectorScanHiddenCameras = _so.FindProperty("_scanHiddenCameras");
				_propCameraSelectorTag = _so.FindProperty("_selectCameraTag");
				_propCameraSelectorName = _so.FindProperty("_selectCameraName");

				_propRenderAntiAliasing = _so.FindProperty("_renderAntiAliasing");
				_propOdsIPD = _so.FindProperty("_odsSettings.ipd");
				_propOdsRender180Degrees = _so.FindProperty("_odsSettings.render180Degrees");
				_propOdsPixelSliceSize = _so.FindProperty("_odsSettings.pixelSliceSize");
				_propOdsPaddingSize = _so.FindProperty("_odsSettings.paddingSize");
				_propOdsCameraClearMode = _so.FindProperty("_odsSettings.cameraClearMode");
				_propOdsCameraClearColor = _so.FindProperty("_odsSettings.cameraClearColor");

#if UNITY_EDITOR_WIN
				_propPostFastStartMp4 = _so.FindProperty("_postCaptureSettings.windows.writeFastStartStreamingForMp4");
#endif
				this.Repaint();
			}
		}

		private void LoadSettings()
		{
			_sourceType = (SourceType)EditorPrefs.GetInt(SettingsPrefix + "SourceType", (int)_sourceType);

			_cameraName = EditorPrefs.GetString(SettingsPrefix + "CameraName", string.Empty);
			_captureModeIndex = EditorPrefs.GetInt(SettingsPrefix + "CaptureModeIndex", 0);

			_captureMouseCursor = EditorPrefs.GetBool(SettingsPrefix + "CaptureMouseCursor", false);
			string mouseCursorGuid = EditorPrefs.GetString(SettingsPrefix + "CaptureMouseTexture", string.Empty);
			if (!string.IsNullOrEmpty(mouseCursorGuid))
			{
				string mouseCursorPath = AssetDatabase.GUIDToAssetPath(mouseCursorGuid);
				if (!string.IsNullOrEmpty(mouseCursorPath))
				{
					_mouseCursorTexture = (Texture2D)AssetDatabase.LoadAssetAtPath(mouseCursorPath, typeof(Texture2D));
				}
			}

			_outputType = (CaptureBase.OutputType)EditorPrefs.GetInt(SettingsPrefix + "OutputType", (int)_outputType);
			_imageSequenceFormat = (ImageSequenceFormat)EditorPrefs.GetInt(SettingsPrefix + "ImageSequenceFormat", (int)_imageSequenceFormat);
			_namedPipePath = EditorPrefs.GetString(SettingsPrefix + "NamedPipePath", _namedPipePath);
			_filenamePrefixFromSceneName = EditorPrefs.GetBool(SettingsPrefix + "FilenamePrefixFromScenename", _filenamePrefixFromSceneName);
			_filenamePrefix = EditorPrefs.GetString(SettingsPrefix + "FilenamePrefix", "capture");
			_filenameExtension = EditorPrefs.GetString(SettingsPrefix + "FilenameExtension", _filenameExtension);
			_fileContainerIndex = EditorPrefs.GetInt(SettingsPrefix + "FileContainerIndex", _fileContainerIndex);
			_appendTimestamp = EditorPrefs.GetBool(SettingsPrefix + "AppendTimestamp", true);
			_imageSequenceStartFrame = EditorPrefs.GetInt(SettingsPrefix + "ImageSequenceStartFrame", 0);
			_imageSequenceZeroDigits = EditorPrefs.GetInt(SettingsPrefix + "ImageSequenceZeroDigits", 6);

			_outputFolderIndex = EditorPrefs.GetInt(SettingsPrefix + "OutputFolderIndex", (int)CaptureBase.OutputPath.RelativeToProject);
			_outputFolderRelative = EditorPrefs.GetString(SettingsPrefix + "OutputFolderRelative", "Captures");
			_outputFolderAbsolute = EditorPrefs.GetString(SettingsPrefix + "OutputFolderAbsolute", string.Empty);

			_downScaleIndex = EditorPrefs.GetInt(SettingsPrefix + "DownScaleIndex", 0);
			_downscaleX = EditorPrefs.GetInt(SettingsPrefix + "DownScaleX", 1);
			_downscaleY = EditorPrefs.GetInt(SettingsPrefix + "DownScaleY", 1);
			_frameRate = EditorPrefs.GetFloat(SettingsPrefix + "FrameRate", _frameRate);
			_timelapseScale = EditorPrefs.GetInt(SettingsPrefix + "TimelapseScale", 1);
			_supportAlpha = EditorPrefs.GetBool(SettingsPrefix + "SupportAlpha", false);
			_useMediaFoundationH264 = EditorPrefs.GetBool(SettingsPrefix + "UseMediaFoundationH264", true);
#if UNITY_EDITOR_WIN
			_videoCodecIndex = EditorPrefs.GetInt(SettingsPrefix + "VideoCodecIndex", 2);	// Set to H.264 by default
#else
			_videoCodecIndex = EditorPrefs.GetInt(SettingsPrefix + "VideoCodecIndex", 0);
#endif


			_renderResolution = (CaptureBase.Resolution)EditorPrefs.GetInt(SettingsPrefix + "RenderResolution", (int)_renderResolution);
			_renderSize.x = EditorPrefs.GetInt(SettingsPrefix + "RenderWidth", 0);
			_renderSize.y = EditorPrefs.GetInt(SettingsPrefix + "RenderHeight", 0);
			_renderAntiAliasing = EditorPrefs.GetInt(SettingsPrefix + "RenderAntiAliasing", 0);
			_useContributingCameras = EditorPrefs.GetBool(SettingsPrefix + "UseContributingCameras", true);

			_captureAudio = EditorPrefs.GetBool(SettingsPrefix + "CaptureAudio", false);
			_audioCodecIndex = EditorPrefs.GetInt(SettingsPrefix + "AudioCodecIndex", 0);
			_audioDeviceIndex = EditorPrefs.GetInt(SettingsPrefix + "AudioDeviceIndex", 0);

			_useMotionBlur = EditorPrefs.GetBool(SettingsPrefix + "UseMotionBlur", false);
			_motionBlurSampleCount = EditorPrefs.GetInt(SettingsPrefix + "MotionBlurSampleCount", 16);

			_render180Degrees = EditorPrefs.GetBool(SettingsPrefix + "Render180Degrees", false);
			_captureWorldSpaceGUI = EditorPrefs.GetBool(SettingsPrefix + "CaptureWorldSpaceGUI", false);
			_supportCameraRotation = EditorPrefs.GetBool(SettingsPrefix + "SupportCameraRotation", false);
			_onlyLeftRightRotation = EditorPrefs.GetBool(SettingsPrefix + "OnlyLeftRightRotation", false);
			_cubemapResolution = EditorPrefs.GetInt(SettingsPrefix + "CubemapResolution", 2048);
			_cubemapDepth = EditorPrefs.GetInt(SettingsPrefix + "CubemapDepth", 24);
			_cubemapStereoPacking = EditorPrefs.GetInt(SettingsPrefix + "CubemapStereoPacking", 0);
			_cubemapStereoIPD = EditorPrefs.GetFloat(SettingsPrefix + "CubemapStereoIPD", 0.064f);

			_startDelay = (StartDelayMode)EditorPrefs.GetInt(SettingsPrefix + "StartDelay", (int)_startDelay);
			_startDelaySeconds = EditorPrefs.GetFloat(SettingsPrefix + "StartDelaySeconds", _startDelaySeconds);

			_stopMode = (StopMode)EditorPrefs.GetInt(SettingsPrefix + "StopMode", (int)_stopMode);
			_stopFrames = EditorPrefs.GetInt(SettingsPrefix + "StopFrames", _stopFrames);
			_stopSeconds = EditorPrefs.GetFloat(SettingsPrefix + "StopSeconds", _stopSeconds);

			_postCaptureSettings.windows.writeFastStartStreamingForMp4 = EditorPrefs.GetBool(SettingsPrefix + "PostFastStartMp4", _postCaptureSettings.windows.writeFastStartStreamingForMp4);

			if (!string.IsNullOrEmpty(_cameraName))
			{
				Camera[] cameras = (Camera[])GameObject.FindObjectsOfType(typeof(Camera));
				foreach (Camera cam in cameras)
				{
					if (cam.name == _cameraName)
					{
						_cameraNode = cam;
						break;
					}
				}
			}

			// Check ranges
			if (_videoCodecIndex >= _videoCodecNames.Length)
			{
				_videoCodecIndex = 0;
			}
			if (_audioDeviceIndex >= _audioDeviceNames.Length)
			{
				_audioDeviceIndex = 0;
				_captureAudio = false;
			}
			if (_audioCodecIndex >= _audioCodecNames.Length)
			{
				_audioCodecIndex = 0;
				_captureAudio = false;
			}

			UpdateFileExtension();

			_showAlpha = EditorPrefs.GetBool(SettingsPrefix + "ShowAlphaChannel", false);

			// Camera selector
			_selectBy = (CameraSelector.SelectByMode)EditorPrefs.GetInt(SelectorPrefix + "SelectBy", (int)_selectBy);
			_scanFrequency = (CameraSelector.ScanFrequencyMode)EditorPrefs.GetInt(SelectorPrefix + "ScanFrequency", (int)_scanFrequency);
			_scanHiddenCameras = EditorPrefs.GetBool(SelectorPrefix + "ScanHiddenCameras", _scanHiddenCameras);
			_selectCameraTag = EditorPrefs.GetString(SelectorPrefix + "Tag", _selectCameraTag);
			_selectCameraName = EditorPrefs.GetString(SelectorPrefix + "Name", _selectCameraName);
		}

		private void SaveSettings()
		{
			EditorPrefs.SetInt(SettingsPrefix + "SourceType", (int)_sourceType);
			EditorPrefs.SetString(SettingsPrefix + "CameraName", _cameraName);
			EditorPrefs.SetInt(SettingsPrefix + "CaptureModeIndex", _captureModeIndex);
			EditorPrefs.SetBool(SettingsPrefix + "CaptureMouseCursor", _captureMouseCursor);
			string mouseCursorGuid = AssetDatabase.AssetPathToGUID(AssetDatabase.GetAssetPath(_mouseCursorTexture));
			EditorPrefs.SetString(SettingsPrefix + "CaptureMouseTexture", mouseCursorGuid);

			EditorPrefs.SetInt(SettingsPrefix + "OutputType", (int)_outputType);
			EditorPrefs.SetInt(SettingsPrefix + "ImageSequenceFormat", (int)_imageSequenceFormat);
			EditorPrefs.SetString(SettingsPrefix + "NamedPipePath", _namedPipePath);
			EditorPrefs.SetBool(SettingsPrefix + "FilenamePrefixFromScenename", _filenamePrefixFromSceneName);
			EditorPrefs.SetString(SettingsPrefix + "FilenamePrefix", _filenamePrefix);
			EditorPrefs.SetString(SettingsPrefix + "FilenameExtension", _filenameExtension);
			EditorPrefs.SetInt(SettingsPrefix + "FileContainerIndex", _fileContainerIndex);
			EditorPrefs.SetBool(SettingsPrefix + "AppendTimestamp", _appendTimestamp);
			EditorPrefs.SetInt(SettingsPrefix + "ImageSequenceStartFrame", _imageSequenceStartFrame);
			EditorPrefs.SetInt(SettingsPrefix + "ImageSequenceZeroDigits", _imageSequenceZeroDigits);

			EditorPrefs.SetInt(SettingsPrefix + "OutputFolderIndex", _outputFolderIndex);
			EditorPrefs.SetString(SettingsPrefix + "OutputFolderRelative", _outputFolderRelative);
			EditorPrefs.SetString(SettingsPrefix + "OutputFolderAbsolute", _outputFolderAbsolute);

			EditorPrefs.SetInt(SettingsPrefix + "DownScaleIndex", _downScaleIndex);
			EditorPrefs.SetInt(SettingsPrefix + "DownScaleX", _downscaleX);
			EditorPrefs.SetInt(SettingsPrefix + "DownScaleY", _downscaleY);
			EditorPrefs.SetBool(SettingsPrefix + "SupportAlpha", _supportAlpha);
			EditorPrefs.SetBool(SettingsPrefix + "UseMediaFoundationH264", _useMediaFoundationH264);
			EditorPrefs.SetFloat(SettingsPrefix + "FrameRate", _frameRate);
			EditorPrefs.SetInt(SettingsPrefix + "TimelapseScale", _timelapseScale);
			EditorPrefs.SetInt(SettingsPrefix + "VideoCodecIndex", _videoCodecIndex);

			EditorPrefs.SetInt(SettingsPrefix + "RenderResolution", (int)_renderResolution);
			EditorPrefs.SetInt(SettingsPrefix + "RenderWidth", (int)_renderSize.x);
			EditorPrefs.SetInt(SettingsPrefix + "RenderHeight", (int)_renderSize.y);
			EditorPrefs.SetInt(SettingsPrefix + "RenderAntiAliasing", _renderAntiAliasing);
			EditorPrefs.SetBool(SettingsPrefix + "UseContributingCameras", _useContributingCameras);

			EditorPrefs.SetBool(SettingsPrefix + "CaptureAudio", _captureAudio);
			EditorPrefs.SetInt(SettingsPrefix + "AudioCodecIndex", _audioCodecIndex);
			EditorPrefs.SetInt(SettingsPrefix + "AudioDeviceIndex", _audioDeviceIndex);

			EditorPrefs.SetBool(SettingsPrefix + "UseMotionBlur", _useMotionBlur);
			EditorPrefs.SetInt(SettingsPrefix + "MotionBlurSampleCount", _motionBlurSampleCount);

			EditorPrefs.SetBool(SettingsPrefix + "Render180Degrees", _render180Degrees);
			EditorPrefs.SetBool(SettingsPrefix + "CaptureWorldSpaceGUI", _captureWorldSpaceGUI);
			EditorPrefs.SetBool(SettingsPrefix + "SupportCameraRotation", _supportCameraRotation);
			EditorPrefs.SetBool(SettingsPrefix + "OnlyLeftRightRotation", _onlyLeftRightRotation);
			EditorPrefs.SetInt(SettingsPrefix + "CubemapResolution", _cubemapResolution);
			EditorPrefs.SetInt(SettingsPrefix + "CubemapDepth", _cubemapDepth);
			EditorPrefs.SetInt(SettingsPrefix + "CubemapStereoPacking", _cubemapStereoPacking);
			EditorPrefs.SetFloat(SettingsPrefix + "CubemapStereoIPD", _cubemapStereoIPD);

			EditorPrefs.SetInt(SettingsPrefix + "StartDelay", (int)_startDelay);
			EditorPrefs.SetFloat(SettingsPrefix + "StartDelaySeconds", _startDelaySeconds);

			EditorPrefs.SetInt(SettingsPrefix + "StopMode", (int)_stopMode);
			EditorPrefs.SetInt(SettingsPrefix + "StopFrames", _stopFrames);
			EditorPrefs.SetFloat(SettingsPrefix + "StopSeconds", _stopSeconds);

			EditorPrefs.SetBool(SettingsPrefix + "PostFastStartMp4", _postCaptureSettings.windows.writeFastStartStreamingForMp4);

			EditorPrefs.SetBool(SettingsPrefix + "ShowAlphaChannel", _showAlpha);

			// Camera selector
			EditorPrefs.SetInt(SelectorPrefix + "SelectBy", (int)_selectBy);
			EditorPrefs.SetInt(SelectorPrefix + "ScanFrequency", (int)_scanFrequency);
			EditorPrefs.SetBool(SelectorPrefix + "ScanHiddenCameras", _scanHiddenCameras);
			EditorPrefs.SetString(SelectorPrefix + "Tag", _selectCameraTag);
			EditorPrefs.SetString(SelectorPrefix + "Name", _selectCameraName);
		}

		private void ResetSettings()
		{
			_sourceType = SourceType.Screen;
			_cameraNode = null;
			_cameraName = string.Empty;
			_captureModeIndex = 0;
			_captureMouseCursor = false;
			_mouseCursorTexture = null;
			_outputType = CaptureBase.OutputType.VideoFile;
			_imageSequenceFormat = ImageSequenceFormat.PNG;
			_namedPipePath = @"\\.\pipe\test_pipe";
			_filenamePrefixFromSceneName = true;
			_filenamePrefix = "capture";
#if UNITY_EDITOR_WIN
			_filenameExtension = "avi";
#else
			_filenameExtension = "mp4";
#endif
			_imageSequenceStartFrame = 0;
			_imageSequenceZeroDigits = 6;
			_outputFolderIndex = (int)CaptureBase.OutputPath.RelativeToProject;
			_outputFolderRelative = "Captures";
			_outputFolderAbsolute = string.Empty;
			_appendTimestamp = true;
			_downScaleIndex = 0;
			_downscaleX = 1;
			_downscaleY = 1;
			_frameRate = 30f;
			_timelapseScale = 1;
			_supportAlpha = false;
			_useMediaFoundationH264 = true;
			_videoCodecIndex = 0;
#if UNITY_EDITOR_WIN
			_videoCodecIndex = 2;			// Set to MF H.264 by default
#endif
			_renderResolution = CaptureBase.Resolution.Original;
			_renderSize = Vector2.one;
			_renderAntiAliasing = 0;
			_useContributingCameras = true;
			_captureAudio = false;
			_audioCodecIndex = 0;
			_audioDeviceIndex = 0;
			_useMotionBlur = false;
			_motionBlurSampleCount = 16;
			_render180Degrees = false;
			_captureWorldSpaceGUI = false;
			_supportCameraRotation = false;
			_onlyLeftRightRotation = false;
			_cubemapResolution = 2048;
			_cubemapDepth = 24;
			_cubemapStereoPacking = 0;
			_startDelay = StartDelayMode.None;
			_startDelaySeconds = 0f;
			_stopMode = StopMode.None;
			_cubemapStereoIPD = 0.064f;
			_stopFrames = 300;
			_stopSeconds = 10f;
			_postCaptureSettings = new CaptureBase.PostCaptureSettings();
			_odsSettings = new CaptureFromCamera360ODS.Settings();
			UpdateFileExtension();

			// Camera selector
			_selectBy = CameraSelector.SelectByMode.HighestDepthCamera;
			_scanFrequency = CameraSelector.ScanFrequencyMode.SceneLoad;
			_scanHiddenCameras = false;
			_selectCameraTag = "MainCamera";
			_selectCameraName = "Main Camera";
		}

		private void Configure(CaptureBase capture)
		{
			capture.VideoCodecPriorityWindows = new string[0];
			capture.VideoCodecPriorityMacOS = new string[0];
			capture._audioCodecPriority = new string[0];

			capture._listVideoCodecsOnStart = false;
			capture.FrameRate = _frameRate;
			capture.TimelapseScale = _timelapseScale;
			capture._supportAlpha = _supportAlpha;
			capture._downScale = GetDownScaleFromIndex(_downScaleIndex);
			if (capture._downScale == CaptureBase.DownScale.Custom)
			{
				capture._maxVideoSize.x = _downscaleX;
				capture._maxVideoSize.y = _downscaleY;
			}

			capture.StartDelay = _startDelay;
			capture.StartDelaySeconds = _startDelaySeconds;
			capture._stopMode = _stopMode;
			capture._stopFrames = _stopFrames;
			capture._stopSeconds = _stopSeconds;
			capture.PostCapture.windows.writeFastStartStreamingForMp4 = _postCaptureSettings.windows.writeFastStartStreamingForMp4;

			capture._isRealTime = (_captureModeIndex == 0);

			capture._outputType = _outputType;
			if (_outputType == CaptureBase.OutputType.VideoFile)
			{
				capture._filenamePrefix = _filenamePrefix;
				capture._appendFilenameTimestamp  = _appendTimestamp;
				capture._allowManualFileExtension = true;
				capture._filenameExtension = _filenameExtension;
			}
			else if (_outputType == CaptureBase.OutputType.NamedPipe)
			{
				capture._namedPipePath = _namedPipePath;
			}
			else if (_outputType == CaptureBase.OutputType.ImageSequence)
			{
				capture.NativeImageSequenceFormat = _imageSequenceFormat;
				capture._imageSequenceStartFrame = _imageSequenceStartFrame;
				capture._imageSequenceZeroDigits = _imageSequenceZeroDigits;
				capture._filenamePrefix = _filenamePrefix;
			}

			if (_outputFolderIndex == (int)CaptureBase.OutputPath.RelativeToPeristentData)
			{
				capture._outputFolderType = CaptureBase.OutputPath.RelativeToPeristentData;
				capture._outputFolderPath = _outputFolderRelative;
			}
			else if (_outputFolderIndex == (int)CaptureBase.OutputPath.Absolute)
			{
				capture._outputFolderType = CaptureBase.OutputPath.Absolute;
				capture._outputFolderPath = _outputFolderAbsolute;
			}
			else if (_outputFolderIndex == (int)CaptureBase.OutputPath.RelativeToDesktop)
			{
				capture._outputFolderType = CaptureBase.OutputPath.RelativeToDesktop;
				capture._outputFolderPath = _outputFolderRelative;
			}
			else
			{
				capture._outputFolderType = CaptureBase.OutputPath.RelativeToProject;
				capture._outputFolderPath = _outputFolderRelative;
			}

#if UNITY_EDITOR_OSX
			capture.NativeForceVideoCodecIndex = capture._codecIndex = Mathf.Max(-1, _videoCodecIndex);
			capture._useMediaFoundationH264 = false;
			capture._noAudio = !_captureAudio;
			capture._forceAudioCodecIndex = capture._audioCodecIndex = Mathf.Max(-1, _audioCodecIndex);
			capture._forceAudioDeviceIndex = capture._audioDeviceIndex = Mathf.Max(-1, _audioDeviceIndex - 2);
#elif UNITY_EDITOR_WIN
			capture.NativeForceVideoCodecIndex = capture._codecIndex = Mathf.Max(-1, (_videoCodecIndex - 4));
			capture._useMediaFoundationH264 = (_videoCodecIndex == 2);
			capture._noAudio = !_captureAudio;
			capture._forceAudioCodecIndex = capture._audioCodecIndex = Mathf.Max(-1, (_audioCodecIndex - 2));
			capture._forceAudioDeviceIndex = capture._audioDeviceIndex = Mathf.Max(-1, (_audioDeviceIndex - 2));
#endif
			if (_useMotionBlur && !capture._isRealTime && Camera.main != null)
			{
				capture._useMotionBlur = _useMotionBlur;
				capture._motionBlurSamples = _motionBlurSampleCount;
				capture._motionBlurCameras = new Camera[1];
				capture._motionBlurCameras[0] = Camera.main;
			}
			else
			{
				capture._useMotionBlur = false;
			}

			if (_captureMouseCursor)
			{
				capture._captureMouseCursor = true;
				if (capture._mouseCursor == null)
				{
					capture._mouseCursor = capture.gameObject.AddComponent<MouseCursor>();
				}
				if (capture._mouseCursor != null)
				{
					capture._mouseCursor.SetTexture(_mouseCursorTexture);
				}
			}
			else
			{
				capture._captureMouseCursor = false;
				if (capture._mouseCursor != null)
				{
					capture._mouseCursor.enabled = false;
				}
			}
		}

		private void CreateComponents()
		{
			// Create hidden gameobject
			if (_gameObject == null)
			{
				_gameObject = GameObject.Find(TempGameObjectName);
				if (_gameObject == null)
				{
					_gameObject = new GameObject(TempGameObjectName);
					_gameObject.hideFlags = HideFlags.HideAndDontSave;
#if UNITY_5 || UNITY_5_4_OR_NEWER
					_gameObject.hideFlags |= HideFlags.DontSaveInBuild|HideFlags.DontSaveInEditor|HideFlags.DontUnloadUnusedAsset;
#endif
					Object.DontDestroyOnLoad(_gameObject);
				}
			}

			// Remove old capture component if different
			if (_captureScreen != null && _sourceType != SourceType.Screen)
			{
				Destroy(_captureScreen);
				_captureScreen = null;
			}
			if (_captureCamera != null && _sourceType != SourceType.Camera)
			{
				Destroy(_captureCamera);
				_captureCamera = null;
			}
			if (_captureCamera360 != null && _sourceType != SourceType.Camera360)
			{
				Destroy(_captureCamera360);
				_captureCamera360 = null;
			}
			if (_captureCamera360ODS != null && _sourceType != SourceType.Camera360ODS)
			{
				Destroy(_captureCamera360ODS);
				_captureCamera360ODS = null;
			}
			if (_cameraSelector != null && _sourceType == SourceType.Screen)
			{
				Destroy(_cameraSelector);
				_cameraSelector = null;
			}

#if AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
			// Remove timelineController for realtime captures
			if (_captureModeIndex == 0)
			{
				if (_timelineController != null)
				{
					Destroy(_timelineController);
					_timelineController = null;
				}
			}
			// Add timelineController for non-realtime captures
			else if (_captureModeIndex == 1)
			{
				if (_timelineController == null)
				{
					_timelineController = _gameObject.AddComponent<TimelineController>();
				}
			}
#endif
			switch (_sourceType)
			{
				case SourceType.Screen:
					if (_captureScreen == null)
					{
						_captureScreen = _gameObject.AddComponent<CaptureFromScreen>();
					}
					_capture = _captureScreen;
					break;
				case SourceType.Camera:
					if (_captureCamera == null)
					{
						_captureCamera = _gameObject.AddComponent<CaptureFromCamera>();
					}
					if (_cameraSelector == null)
					{
						_cameraSelector = _gameObject.AddComponent<CameraSelector>();
					}
					SetupCameraSelector();
					_captureCamera.SetCamera(_cameraNode, _useContributingCameras);
					_captureCamera.CameraSelector = _cameraSelector;
					_capture = _captureCamera;
					_capture._renderResolution = _renderResolution;
					_capture._renderSize = _renderSize;
					_capture._renderAntiAliasing = _renderAntiAliasing;
					break;
				case SourceType.Camera360:
					if (_captureCamera360 == null)
					{
						_captureCamera360 = _gameObject.AddComponent<CaptureFromCamera360>();
					}
					if (_cameraSelector == null)
					{
						_cameraSelector = _gameObject.AddComponent<CameraSelector>();
					}
					SetupCameraSelector();
					_capture = _captureCamera360;
					_capture._renderResolution = _renderResolution;
					_capture._renderSize = _renderSize;
					_capture._renderAntiAliasing = _renderAntiAliasing;
					_captureCamera360.SetCamera(_cameraNode);
					_captureCamera360.CameraSelector = _cameraSelector;
					_captureCamera360._render180Degrees = _render180Degrees;
					_captureCamera360._supportCameraRotation = _supportCameraRotation;
					_captureCamera360._onlyLeftRightRotation = _onlyLeftRightRotation;
					_captureCamera360._supportGUI = _captureWorldSpaceGUI;
					_captureCamera360._cubemapResolution = _cubemapResolution;
					_captureCamera360._cubemapDepth = _cubemapDepth;
					_captureCamera360._stereoRendering = (StereoPacking)_cubemapStereoPacking;
					_captureCamera360._ipd = _cubemapStereoIPD;
					break;
				case SourceType.Camera360ODS:
					if (_captureCamera360ODS == null)
					{
						_captureCamera360ODS = _gameObject.AddComponent<CaptureFromCamera360ODS>();
					}
					if (_cameraSelector == null)
					{
						_cameraSelector = _gameObject.AddComponent<CameraSelector>();
					}
					SetupCameraSelector();
					_capture = _captureCamera360ODS;
					_capture._renderResolution = _renderResolution;
					_capture._renderSize = _renderSize;
					_capture._renderAntiAliasing = _renderAntiAliasing;
					_captureCamera360ODS.Setup.camera = _cameraNode;
					_captureCamera360ODS.Setup.cameraSelector = _cameraSelector;
					_captureCamera360ODS.Setup.render180Degrees = _odsSettings.render180Degrees;
					_captureCamera360ODS.Setup.ipd = _odsSettings.ipd;
					_captureCamera360ODS.Setup.pixelSliceSize = _odsSettings.pixelSliceSize;
					_captureCamera360ODS.Setup.paddingSize = _odsSettings.paddingSize;
					_captureCamera360ODS.Setup.cameraClearMode = _odsSettings.cameraClearMode;
					_captureCamera360ODS.Setup.cameraClearColor= _odsSettings.cameraClearColor;
					break;
			}
#if AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
			if (_capture != null)
			{
				_capture.TimelineController = _timelineController;
			}
#endif
		}

		private void SetupCameraSelector()
		{
			if (_cameraSelector == null) return;

			_cameraSelector.SelectBy = _selectBy;
			_cameraSelector.ScanFrequency = _scanFrequency;
			_cameraSelector.ScanHiddenCameras = _scanHiddenCameras;
			if (_selectBy == CameraSelector.SelectByMode.Tag)
			{
				_cameraSelector.SelectTag = _selectCameraTag;
			}
			else if (_selectBy == CameraSelector.SelectByMode.Name)
			{
				_cameraSelector.SelectName = _selectCameraName;
			}
			else if (_selectBy == CameraSelector.SelectByMode.Manual)
			{
				_cameraSelector.Camera = _cameraNode;
			}
		}

		private void CreateGUI()
		{
			try
			{
				if (!NativePlugin.Init())
				{
					Debug.LogError("[AVProMovieCapture] Failed to initialise");
					return;
				}
			}
			catch (System.DllNotFoundException e)
			{
				_isFailedInit = true;
				string missingDllMessage = string.Empty;
#if (UNITY_5 || UNITY_5_4_OR_NEWER)
				missingDllMessage = "Unity couldn't find the plugin DLL. Please select the native plugin files in 'Plugins/RenderHeads/AVProMovieCapture/Plugins' folder and select the correct platform in the Inspector.";
#else
				missingDllMessage = "Unity couldn't find the plugin DLL, Unity 4.x requires the 'Plugins' folder to be at the root of your project.  Please move the contents of the 'Plugins' folder (in Plugins/RenderHeads/AVProMovieCapture/Plugins) to the 'Plugins' folder in the root of your project.";
#endif
				Debug.LogError("[AVProMovieCapture] " + missingDllMessage);
#if UNITY_EDITOR
				UnityEditor.EditorUtility.DisplayDialog("Plugin files not found", missingDllMessage, "Ok");
#endif
				throw e;
			}

			// Video codec enumeration
			{
				int numVideoCodecs = Mathf.Max(0, NativePlugin.GetNumAVIVideoCodecs());
#if UNITY_EDITOR_WIN
				_videoCodecNames = new string[numVideoCodecs + 4];
				_videoCodecNames[0] = "Uncompressed";
				_videoCodecNames[1] = string.Empty;
				_videoCodecNames[2] = "Media Foundation H.264 (MP4)";
				_videoCodecNames[3] = string.Empty;
				_videoCodecConfigurable = new bool[numVideoCodecs + 4];
				_videoCodecConfigurable[0] = false;
				_videoCodecConfigurable[1] = false;
				_videoCodecConfigurable[2] = false;
				_videoCodecConfigurable[3] = false;
				for (int i = 0; i < numVideoCodecs; i++)
				{
					_videoCodecNames[i + 4] = i.ToString("D2") + ") " + NativePlugin.GetAVIVideoCodecName(i).Replace("/", "_");
					_videoCodecConfigurable[i + 4] = NativePlugin.IsConfigureVideoCodecSupported(i);
				}
#else
				_videoCodecNames = new string[numVideoCodecs];
				_videoCodecConfigurable = new bool[numVideoCodecs];
				for (int i = 0; i < numVideoCodecs; i++)
				{
					_videoCodecNames[i] = i.ToString("D2") + ") " + NativePlugin.GetAVIVideoCodecName(i).Replace("/", "_");
					_videoCodecConfigurable[i] = NativePlugin.IsConfigureVideoCodecSupported(i);
				}
#endif
			}

			// Audio device enumeration
			{
				int numAudioDevices = Mathf.Max(0, NativePlugin.GetNumAVIAudioInputDevices());
				_audioDeviceNames = new string[numAudioDevices + 2];
				_audioDeviceNames[0] = "Unity";
				_audioDeviceNames[1] = string.Empty;
				for (int i = 0; i < numAudioDevices; i++)
				{
					_audioDeviceNames[i + 2] = i.ToString("D2") + ") " + NativePlugin.GetAVIAudioInputDeviceName(i).Replace("/", "_");
				}
			}

			// Audio codec enumeration
			{
				int numAudioCodecs = Mathf.Max(0, NativePlugin.GetNumAVIAudioCodecs());
#if UNITY_EDITOR_WIN
				_audioCodecNames = new string[numAudioCodecs + 2];
				_audioCodecNames[0] = "Uncompressed";
				_audioCodecNames[1] = string.Empty;
				_audioCodecConfigurable = new bool[numAudioCodecs + 2];
				_audioCodecConfigurable[0] = false;
				_audioCodecConfigurable[1] = false;
				for (int i = 0; i < numAudioCodecs; i++)
				{
					_audioCodecNames[i + 2] = i.ToString("D2") + ") " + NativePlugin.GetAVIAudioCodecName(i).Replace("/", "_");
					_audioCodecConfigurable[i + 2] = NativePlugin.IsConfigureAudioCodecSupported(i);
				}
#else
				_audioCodecNames = new string[numAudioCodecs];
				_audioCodecConfigurable = new bool[numAudioCodecs];
				for (int i = 0; i < numAudioCodecs; i++)
				{
					_audioCodecNames[i] = i.ToString("D2") + ") " + NativePlugin.GetAVIAudioCodecName(i).Replace("/", "_");
					_audioCodecConfigurable[i] = NativePlugin.IsConfigureAudioCodecSupported(i);
				}
#endif
			}

			_isInit = true;
		}

		private void OnEnable()
		{
			if (_icon == null)
			{
				_icon = Resources.Load<Texture2D>("AVProMovieCaptureIcon");
			}

			if (!_isCreated)
			{
				SetupWindow();
			}

			_isTrialVersion = IsTrialVersion();

			// Check that the plugin version number is not too old
			{
				string pluginVersionString = NativePlugin.GetPluginVersionString();
				_pluginVersionWarningText = string.Empty;
				if (!pluginVersionString.StartsWith(NativePlugin.ExpectedPluginVersion))
				{
					_pluginVersionWarningText = "Warning: Plugin version number " + pluginVersionString + " doesn't match the expected version number " + NativePlugin.ExpectedPluginVersion + ".  It looks like the plugin didn't upgrade correctly.  To resolve this please restart Unity and try to upgrade the package again.";
				}
			}
		}

		private void OnDisable()
		{
			SaveSettings();
			StopCapture();
			if (_gameObject != null)
			{
				DestroyImmediate(_gameObject);
				_gameObject = null;
				_capture = null;
				_captureScreen = null;
				_captureCamera = null;
				_captureCamera360 = null;
				_captureCamera360ODS = null;
				_cameraSelector = null;
				#if AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
				_timelineController = null;
				#endif
			}
			_isInit = false;
			_isCreated = false;
			Repaint();
		}

		private void StartCapture()
		{
			_lastFileSize = 0;
			_lastEncodedSeconds = 0;
			_lastEncodedMinutes = 0;
			_lastEncodedFrame = 0;

			CreateComponents();
			if (_capture != null)
			{
				Configure(_capture);
				_capture.SelectCodec(false);
				if (!_capture._noAudio)
				{
					_capture.SelectAudioCodec(false);
					_capture.SelectAudioDevice(false);
				}
				_capture.QueueStartCapture();
			}
		}

		private void StopCapture(bool cancelCapture = false)
		{
			if (_capture != null)
			{
				if (_capture.IsCapturing())
				{
					if (!cancelCapture)
					{
						_capture.StopCapture();
					}
					else
					{
						_capture.CancelCapture();
					}
				}
				_capture = null;
			}
		}

		// Updates 10 times/second
		void OnInspectorUpdate()
		{
			if (_capture != null)
			{
				if (Application.isPlaying)
				{
					if (_capture.IsCapturing())
					{
						_lastFileSize = _capture.GetCaptureFileSize();
					}

					if (!_capture._isRealTime)
					{
						_lastEncodedSeconds = (uint)Mathf.FloorToInt((float)_capture.NumEncodedFrames / _capture.FrameRate);
					}
					else
					{
						_lastEncodedSeconds = _capture.TotalEncodedSeconds;
					}
					_lastEncodedMinutes = _lastEncodedSeconds / 60;
					_lastEncodedSeconds = _lastEncodedSeconds % 60;
					_lastEncodedFrame = _capture.NumEncodedFrames % (uint)_capture.FrameRate;

					// If the capture has stopped automatically, we need to update the UI
					if (_capture._stopMode != StopMode.None && _capture.NumEncodedFrames > 0 && !_capture.IsCapturing())
					{
						StopCapture();
					}
				}
				else
				{
					StopCapture();
				}
			}
			else
			{
				if (_queueConfigureVideoCodec >= 0)
				{
					int configureVideoCodec = _queueConfigureVideoCodec;
					_queueConfigureVideoCodec = -1;
					NativePlugin.Init();
					NativePlugin.ConfigureVideoCodec(configureVideoCodec);
				}

				if (_queueConfigureAudioCodec >= 0)
				{
					int configureAudioCodec = _queueConfigureAudioCodec;
					_queueConfigureAudioCodec = -1;
					NativePlugin.Init();
					NativePlugin.ConfigureAudioCodec(configureAudioCodec);
				}

				if (_queueStart && Application.isPlaying)
				{
					_queueStart = false;
					StartCapture();
				}
			}

			Repaint();
		}

		private static bool ShowConfigList(string title, string[] items, bool[] isConfigurable, ref int itemIndex, ref bool itemChanged, bool showConfig = true, bool listEnabled = true)
		{
			bool result = false;

			if (itemIndex < 0 || items == null)
				return result;

			if (!string.IsNullOrEmpty(title))
			{
				EditorGUILayout.LabelField(title, EditorStyles.boldLabel);
			}
			EditorGUI.BeginDisabledGroup(!listEnabled);
			EditorGUILayout.BeginHorizontal();
			int newItemIndex = EditorGUILayout.Popup(itemIndex, items);
			itemChanged = (newItemIndex != itemIndex);
			itemIndex = newItemIndex;

#if UNITY_EDITOR_WIN
			if (showConfig && isConfigurable != null && itemIndex < isConfigurable.Length)
			{
				EditorGUI.BeginDisabledGroup(itemIndex == 0 || !isConfigurable[itemIndex]);
				if (GUILayout.Button("Configure"))
				{
					result = true;
				}
				EditorGUI.EndDisabledGroup();
			}
#endif
			EditorGUILayout.EndHorizontal();
			EditorGUI.EndDisabledGroup();

			return result;
		}

		void OnGUI()
		{
			if ((Application.platform != RuntimePlatform.WindowsEditor)
			&&  (Application.platform != RuntimePlatform.OSXEditor))
			{
				EditorGUILayout.LabelField("AVPro Movie Capture only works on the Windows and macOS platforms.");
				return;
			}

			if (!_isInit)
			{
				if (_isFailedInit)
				{
					GUILayout.Label("Error", EditorStyles.boldLabel);
					GUI.enabled = false;

					string missingDllMessage = string.Empty;
#if (UNITY_5 || UNITY_5_4_OR_NEWER)
					missingDllMessage = "Unity couldn't find the plugin DLL. Please select the native plugin files in 'Plugins/RenderHeads/AVProMovieCapture/Plugins' folder and select the correct platform in the Inspector.";
#else
					missingDllMessage = "Unity couldn't find the plugin DLL, Unity 4.x requires the 'Plugins' folder to be at the root of your project.  Please move the contents of the 'Plugins' folder (in Plugins/RenderHeads/AVProMovieCapture/Plugins) to the 'Plugins' folder in the root of your project.";
#endif

					GUILayout.TextArea(missingDllMessage);
					GUI.enabled = true;
					return;
				}
				else
				{
					EditorGUILayout.LabelField("Initialising...");
					return;
				}
			}

			if (!string.IsNullOrEmpty(_pluginVersionWarningText))
			{
				GUI.color = Color.yellow;
				GUILayout.TextArea(_pluginVersionWarningText);
				GUI.color = Color.white;
			}

			if (_so == null)
			{
				return;
			}

			_so.Update();

#if AVPRO_MOVIECAPTURE_GRAPHICSDEVICETYPE_51 && UNITY_EDITOR_WIN
			if (SystemInfo.graphicsDeviceType != UnityEngine.Rendering.GraphicsDeviceType.Direct3D11)
			{
				GUI.color = Color.yellow;
				GUILayout.TextArea("Consider switching to Direct3D11 for best capture results.  You may need to change your Build platform to Windows.");
				GUI.color = Color.white;
			}
#endif

			if (_isTrialVersion)
			{
				EditorUtils.DrawSectionColored("- AVPRO MOVIE CAPTURE - TRIAL VERSION", ref _expandSectionTrial, DrawTrialMessage, Color.magenta, Color.magenta, Color.magenta);
				//EditorGUILayout.Space();
			}

			DrawControlButtonsGUI();
			EditorGUILayout.Space();

			// Live Capture Stats
			if (Application.isPlaying && _capture != null && _capture.IsCapturing())
			{
				if (_propStopMode.enumValueIndex != (int)StopMode.None)
				{
					Rect r = GUILayoutUtility.GetRect(128f, EditorStyles.label.CalcHeight(GUIContent.none, 32f), GUILayout.ExpandWidth(true));
					float progress = _capture.GetProgress();
					EditorGUI.ProgressBar(r, progress, (progress * 100f).ToString("F1") + "%");
				}

				_scroll = EditorGUILayout.BeginScrollView(_scroll);
				DrawBaseCapturingGUI(_capture);
				DrawMoreCapturingGUI();
				EditorGUILayout.EndScrollView();
			}
			// Configuration
			else if (_capture == null)
			{
				string[] _toolNames = { "Settings", "About" };
				_selectedTool = GUILayout.Toolbar(_selectedTool, _toolNames);
				switch (_selectedTool)
				{
					case 0:
						DrawConfigGUI_Toolbar();
						_scroll = EditorGUILayout.BeginScrollView(_scroll);
						DrawConfigGUI();
						EditorGUILayout.EndScrollView();
						break;
					case 1:
						_scroll = EditorGUILayout.BeginScrollView(_scroll);
						DrawConfigGUI_About();
						EditorGUILayout.EndScrollView();
						break;
				}
			}

			if (_so.ApplyModifiedProperties())
			{
				EditorUtility.SetDirty(this);
			}
		}

		private void DrawTrialMessage()
		{
			string message = "The free trial version is watermarked.  Upgrade to the full package to remove the watermark.";

			//GUI.backgroundColor = Color.yellow;
			//EditorGUILayout.BeginVertical(GUI.skin.box);
			//GUI.color = Color.yellow;
			//GUILayout.Label("AVPRO MOVIE CAPTURE - FREE TRIAL VERSION", EditorStyles.boldLabel);
			GUI.color = Color.white;
			GUILayout.Label(message, EditorStyles.wordWrappedLabel);
			if (GUILayout.Button("Upgrade Now"))
			{
				Application.OpenURL("https://www.assetstore.unity3d.com/en/#!/content/2670");
			}
			//EditorGUILayout.EndVertical();
			GUI.backgroundColor = Color.white;
			GUI.color = Color.white;
		}

		private void DrawControlButtonsGUI()
		{
			EditorGUILayout.BeginHorizontal();
			if (_capture == null)
			{
				GUI.backgroundColor = Color.green;
				string startString = "Start Capture";
				if (_captureModeIndex == 1)
				{
					startString = "Start Render";
				}
				if (GUILayout.Button(startString, GUILayout.Height(32f)))
				{
					bool isReady = true;
					if (_sourceType == SourceType.Camera &&
						_cameraNode == null &&
						_selectBy == CameraSelector.SelectByMode.Manual)
					{
						if ((ConfigTabs)_selectedConfigTab != ConfigTabs.Capture)
						{
							_cameraNode = Utils.GetUltimateRenderCamera();
						}
						if (_cameraNode == null)
						{
							Debug.LogError("[AVProMovieCapture] Please select a Camera to capture from, or select to capture from Screen.");
							isReady = false;
						}
					}

					if (isReady)
					{
						if (!Application.isPlaying)
						{
							EditorApplication.isPlaying = true;
							_queueStart = true;
						}
						else
						{
							StartCapture();
							Repaint();
						}
					}
				}
			}
			else
			{
				GUI.backgroundColor = Color.cyan;
				if (GUILayout.Button("Cancel", GUILayout.Height(32f)))
				{
					StopCapture(true);
					Repaint();
				}
				GUI.backgroundColor = Color.red;
				if (GUILayout.Button("Stop", GUILayout.Height(32f)))
				{
					StopCapture(false);
					Repaint();
				}

				if (_capture != null)
				{
					if (_capture.IsPaused())
					{
						GUI.backgroundColor = Color.green;
						if (GUILayout.Button("Resume", GUILayout.Height(32f)))
						{
							_capture.ResumeCapture();
							Repaint();
						}
					}
					else
					{
						GUI.backgroundColor = Color.yellow;
						if (GUILayout.Button("Pause", GUILayout.Height(32f)))
						{
							_capture.PauseCapture();
							Repaint();
						}
					}
				}
			}
			EditorGUILayout.EndHorizontal();

			GUI.backgroundColor = Color.white;

			GUILayout.BeginHorizontal();
			if (GUILayout.Button("Browse"))
			{
				if (!string.IsNullOrEmpty(CaptureBase.LastFileSaved))
				{
					Utils.ShowInExplorer(CaptureBase.LastFileSaved);
				}
			}
			{
				Color prevColor = GUI.color;
				GUI.color = Color.cyan;
				if (GUILayout.Button("View Last Capture"))
				{
					if (!string.IsNullOrEmpty(CaptureBase.LastFileSaved))
					{
						Utils.OpenInDefaultApp(CaptureBase.LastFileSaved);
					}
				}
				GUI.color = prevColor;
			}
			GUILayout.EndHorizontal();
		}


		public static void DrawBaseCapturingGUI(CaptureBase capture)
		{
			GUILayout.Space(8.0f);
			Texture texture = capture.GetPreviewTexture();
			if (texture != null)
			{
				float width = Screen.width - (Screen.width / 8f);
				width = (Screen.width / 2f) - (Screen.width / 16f);
				float aspect = (float)texture.width / (float)texture.height;
				GUILayout.BeginHorizontal();
				GUILayout.FlexibleSpace();

				if (_showAlpha)
				{
					width = (Screen.width / 2f) - (Screen.width / 16f);
					Rect textureRect = GUILayoutUtility.GetRect(width, width / aspect, GUILayout.ExpandWidth(false), GUILayout.ExpandHeight(false));
					EditorGUI.DrawPreviewTexture(textureRect, texture, null, ScaleMode.ScaleToFit);
					//textureRect = GUILayoutUtility.GetRect(width, width / aspect);
					textureRect = GUILayoutUtility.GetRect(width, width / aspect, GUILayout.ExpandWidth(false), GUILayout.ExpandHeight(false)); ;
					EditorGUI.DrawTextureAlpha(textureRect, texture, ScaleMode.ScaleToFit);
				}
				else
				{
					Rect textureRect = GUILayoutUtility.GetRect(width, width / aspect, GUILayout.ExpandWidth(false), GUILayout.ExpandHeight(false));
					EditorGUI.DrawPreviewTexture(textureRect, texture, null, ScaleMode.ScaleToFit);
				}
				GUILayout.FlexibleSpace();
				GUILayout.EndHorizontal();

				GUILayout.BeginHorizontal();
				GUILayout.FlexibleSpace();
				_showAlpha = GUILayout.Toggle(_showAlpha, "Show Alpha", GUILayout.ExpandWidth(false));
				GUILayout.FlexibleSpace();
				GUILayout.EndHorizontal();
				GUILayout.Space(8.0f);
			}

			GUILayout.Label("Output", EditorStyles.boldLabel);
			EditorGUILayout.BeginVertical("box");
			EditorGUI.indentLevel++;

			GUILayout.Label("Recording to: " + System.IO.Path.GetFileName(capture.LastFilePath), EditorStyles.wordWrappedLabel);
			GUILayout.Space(8.0f);

			GUILayout.Label("Video");
			EditorGUILayout.LabelField("Dimensions", capture.GetRecordingWidth() + "x" + capture.GetRecordingHeight() + " @ " + capture.FrameRate.ToString("F2") + "hz");
			if (capture._outputType == CaptureBase.OutputType.VideoFile)
			{
#if UNITY_EDITOR_WIN
				if (capture._useMediaFoundationH264)
				{
					EditorGUILayout.LabelField("Codec", "Media Foundation H.264");
				}
				else
#endif
				{
					EditorGUILayout.LabelField("Codec", capture._codecName);
				}
			}
			else if (capture._outputType == CaptureBase.OutputType.ImageSequence)
			{
				EditorGUILayout.LabelField("Codec", capture.NativeImageSequenceFormat.ToString());
			}

			if (!capture._noAudio && capture._isRealTime)
			{
				GUILayout.Label("Audio");
				EditorGUILayout.LabelField("Source", capture._audioDeviceName);
				EditorGUILayout.LabelField("Codec", capture._audioCodecName);
				if (capture._audioDeviceName == "Unity")
				{
					EditorGUILayout.LabelField("Sample Rate", capture._unityAudioSampleRate.ToString() + "hz");
					EditorGUILayout.LabelField("Channels", capture._unityAudioChannelCount.ToString());
				}
			}

			EditorGUI.indentLevel--;
			EditorGUILayout.EndVertical();

			GUILayout.Space(8.0f);

			GUILayout.Label("Stats", EditorStyles.boldLabel);
			EditorGUILayout.BeginVertical("box");
			EditorGUI.indentLevel++;

			if (capture.FPS > 0f)
			{
				Color originalColor = GUI.color;
				if (capture._isRealTime)
				{
					float fpsDelta = (capture.FPS - capture.FrameRate);
					GUI.color = Color.red;
					if (fpsDelta > -10)
					{
						GUI.color = Color.yellow;
					}
					if (fpsDelta > -2)
					{
						GUI.color = Color.green;
					}
				}

				EditorGUILayout.LabelField("Capture Rate", string.Format("{0:0.##} / {1:F2} FPS", capture.FPS, capture.FrameRate));

				GUI.color = originalColor;
			}
			else
			{
				EditorGUILayout.LabelField("Capture Rate", string.Format(".. / {0:F2} FPS", capture.FrameRate));
			}

			EditorGUILayout.LabelField("Encoded Frames", capture.NumEncodedFrames.ToString());

			EditorGUI.indentLevel--;
			EditorGUILayout.EndVertical();
		}

		public void DrawMoreCapturingGUI()
		{
			GUILayout.Label("More Stats", EditorStyles.boldLabel);
			EditorGUILayout.BeginVertical("box");
			EditorGUI.indentLevel++;

			EditorGUILayout.LabelField("File Size", ((float)_lastFileSize / (1024f * 1024f)).ToString("F1") + "MB");
			EditorGUILayout.LabelField("Video Length", _lastEncodedMinutes.ToString("00") + ":" + _lastEncodedSeconds.ToString("00") + "." + _lastEncodedFrame.ToString("000"));

			GUILayout.Label("Dropped Frames");
			EditorGUILayout.LabelField("In Unity", _capture.NumDroppedFrames.ToString());
			EditorGUILayout.LabelField("In Encoder", _capture.NumDroppedEncoderFrames.ToString());
			if (!_capture._noAudio && _capture._isRealTime)
			{
				if (_capture._audioCapture && _capture._audioDeviceName == "Unity")
				{
					EditorGUILayout.LabelField("Audio Overflows", _capture._audioCapture.OverflowCount.ToString());
				}
			}

			EditorGUI.indentLevel--;
			EditorGUILayout.EndVertical();
		}

		private void DrawConfigGUI_Toolbar()
		{
			_selectedConfigTab = GUILayout.Toolbar(_selectedConfigTab, _tabNames);
		}

		private void DrawConfigGUI()
		{
			switch ((ConfigTabs)_selectedConfigTab)
			{
				case ConfigTabs.Encoding:
					DrawConfigGUI_Encoding();
					break;
				case ConfigTabs.Capture:
					DrawConfigGUI_Capture();
					break;
				case ConfigTabs.Visual:
					DrawConfigGUI_Visual();
					break;
				case ConfigTabs.Audio:
					DrawConfigGUI_Audio();
					break;
			}

			GUILayout.FlexibleSpace();
		}

		public static void DrawConfigGUI_About()
		{
			string version = NativePlugin.GetPluginVersionString();

			EditorGUILayout.BeginHorizontal();
			GUILayout.FlexibleSpace();

			if (_icon == null)
			{
				_icon = Resources.Load<Texture2D>("AVProMovieCaptureIcon");
			}
			if (_icon != null)
			{
				GUILayout.Label(new GUIContent(_icon));
			}
			GUILayout.FlexibleSpace();
			EditorGUILayout.EndHorizontal();

			EditorGUILayout.BeginHorizontal();
			GUILayout.FlexibleSpace();
			GUI.color = Color.yellow;
			GUILayout.Label("AVPro Movie Capture by RenderHeads Ltd", EditorStyles.boldLabel);
			GUI.color = Color.white;
			GUILayout.FlexibleSpace();
			EditorGUILayout.EndHorizontal();

			EditorGUILayout.BeginHorizontal();
			GUILayout.FlexibleSpace();
			GUI.color = Color.yellow;
			GUILayout.Label("version " + version + " (scripts v" + NativePlugin.ScriptVersion + ")");
			GUI.color = Color.white;
			GUILayout.FlexibleSpace();
			EditorGUILayout.EndHorizontal();

			// Links
			{
				GUILayout.Space(32f);
				GUI.backgroundColor = Color.white;

				EditorGUILayout.LabelField("AVPro Movie Capture Links", EditorStyles.boldLabel);

				GUILayout.Space(8f);

				EditorGUILayout.LabelField("Documentation");
				EditorGUILayout.BeginHorizontal();
				if (GUILayout.Button("User Manual", GUILayout.ExpandWidth(false)))
				{
					Application.OpenURL(LinkUserManual);
				}
				EditorGUILayout.EndHorizontal();


				GUILayout.Space(16f);

				GUILayout.Label("Rate and Review (★★★★☆)", GUILayout.ExpandWidth(false));
				if (GUILayout.Button("Unity Asset Store Page", GUILayout.ExpandWidth(false)))
				{
					if (!_isTrialVersion)
					{
						Application.OpenURL(LinkAssetStorePage);
					}
					else
					{
						Application.OpenURL(LinkFreeAssetStorePage);
					}
				}

				GUILayout.Space(16f);

				GUILayout.Label("Community");
				if (GUILayout.Button("Unity Forum Page", GUILayout.ExpandWidth(false)))
				{
					Application.OpenURL(LinkForumPage);
				}

				GUILayout.Space(16f);

				GUILayout.Label("Homepage", GUILayout.ExpandWidth(false));
				if (GUILayout.Button("AVPro Movie Capture Website", GUILayout.ExpandWidth(false)))
				{
					Application.OpenURL(LinkPluginWebsite);
				}

				GUILayout.Space(16f);

				GUILayout.Label("Bugs and Support");
				EditorGUILayout.BeginHorizontal();
				if (GUILayout.Button("GitHub Issues", GUILayout.ExpandWidth(false)))
				{
					Application.OpenURL(LinkSupport);
				}
				EditorGUILayout.EndHorizontal();
			}

			// Credits
			{
				GUILayout.Space(32f);
				EditorGUILayout.LabelField("Credits", EditorStyles.boldLabel);
				GUILayout.Space(8f);
				EditorUtils.CentreLabel("Programming", EditorStyles.boldLabel);
				EditorUtils.CentreLabel("Andrew Griffiths");
				EditorUtils.CentreLabel("Morris Butler");
				EditorUtils.CentreLabel("Sunrise Wang");
				GUILayout.Space(8f);
				EditorUtils.CentreLabel("Graphics", EditorStyles.boldLabel);
				EditorUtils.CentreLabel("Jeff Rusch");
				EditorUtils.CentreLabel("Luke Godward");
			}

			// Bug reporting
			{
				GUILayout.Space(32f);

				EditorGUILayout.LabelField("Bug Reporting Notes", EditorStyles.boldLabel);

				EditorGUILayout.SelectableLabel(SupportMessage, EditorStyles.wordWrappedLabel, GUILayout.Height(180f));
			}
		}

		private void DrawConfigGUI_Capture()
		{
			//GUILayout.Label("Capture", EditorStyles.boldLabel);
			EditorGUILayout.BeginVertical("box");
			//EditorGUI.indentLevel++;

			// Time
			{
				GUILayout.Space(8f);
				EditorGUILayout.LabelField("Time", EditorStyles.boldLabel);
				EditorGUI.indentLevel++;
				_captureModeIndex = EditorGUILayout.Popup("Capture Mode", _captureModeIndex, _captureModes);
				GUILayout.BeginHorizontal();
				EditorGUILayout.PropertyField(_propFrameRate, GUILayout.ExpandWidth(false));
				_propFrameRate.floatValue = Mathf.Clamp(_propFrameRate.floatValue, 0.01f, 240f);
				EditorUtils.FloatAsPopup("▶", "Common Frame Rates", _so, _propFrameRate, EditorUtils.CommonFrameRateNames, EditorUtils.CommonFrameRateValues);
				GUILayout.EndHorizontal();
				if (_captureModeIndex == 0)
				{
					EditorGUILayout.PropertyField(_propTimelapseScale);
					_propTimelapseScale.intValue = Mathf.Max(1, _propTimelapseScale.intValue);
				}
				EditorGUI.indentLevel--;
			}

			// Source
			GUILayout.Space(8f);
			EditorGUILayout.LabelField("Source", EditorStyles.boldLabel);
			EditorGUI.indentLevel++;
			EditorUtils.EnumAsDropdown("Source", _propSourceType, _sourceNames);

			if (_sourceType == SourceType.Camera360ODS && _captureModeIndex == 0)
			{
				GUI.color = Color.yellow;
				GUILayout.TextArea("Warning: This source type is very slow and not suitable for 'Realtime Capture'.  Consider changing the capture mode to 'Offline Render'.");
				GUI.color = Color.white;
			}

			EditorGUI.indentLevel--;

			//_sourceType = (SourceType)EditorGUILayout.EnumPopup("Type", _sourceType);
			if (_sourceType == SourceType.Camera || _sourceType == SourceType.Camera360 || _sourceType == SourceType.Camera360ODS)
			{
				GUILayout.Space(8f);
				EditorGUILayout.LabelField("Camera Selector", EditorStyles.boldLabel);
				EditorGUI.indentLevel++;

				EditorGUILayout.PropertyField(_propCameraSelectorSelectBy);
				if (_propCameraSelectorSelectBy.enumValueIndex == (int)CameraSelector.SelectByMode.Name)
				{
					EditorGUILayout.PropertyField(_propCameraSelectorName, _guiCameraSelectorName);

				}
				else if (_propCameraSelectorSelectBy.enumValueIndex == (int)CameraSelector.SelectByMode.Tag)
				{
					EditorGUILayout.PropertyField(_propCameraSelectorTag, _guiCameraSelectorTag);
				}
				else if (_propCameraSelectorSelectBy.enumValueIndex == (int)CameraSelector.SelectByMode.Manual)
				{
					if (_cameraNode == null)
					{
						_cameraNode = Utils.GetUltimateRenderCamera();
					}
					_cameraNode = (Camera)EditorGUILayout.ObjectField("Camera", _cameraNode, typeof(Camera), true);
				}

				if (_sourceType == SourceType.Camera && _cameraNode != null)
				{
					EditorGUILayout.PropertyField(_propUseContributingCameras, _guiContributingCameras);
				}

				EditorGUILayout.PropertyField(_propCameraSelectorScanFrequency);
				EditorGUILayout.PropertyField(_propCameraSelectorScanHiddenCameras);

				EditorGUI.indentLevel--;
			}


			// Screen options
			if (_sourceType == SourceType.Screen)
			{
				GUILayout.Space(8f);
				EditorGUILayout.LabelField("Cursor", EditorStyles.boldLabel);
				EditorGUI.indentLevel++;
				_captureMouseCursor = EditorGUILayout.Toggle("Capture Mouse Cursor", _captureMouseCursor);
				_mouseCursorTexture = (Texture2D)EditorGUILayout.ObjectField("Mouse Cursor Texture", _mouseCursorTexture, typeof(Texture2D), false);
				EditorGUI.indentLevel--;
			}

			// Camera overrides
			if (_sourceType == SourceType.Camera || _sourceType == SourceType.Camera360 || _sourceType == SourceType.Camera360ODS)
			{
				GUILayout.Space(8f);
				EditorGUILayout.LabelField("Camera Overrides", EditorStyles.boldLabel);
				EditorGUI.indentLevel++;

				{
					EditorUtils.EnumAsDropdown("Resolution", _propRenderResolution, CaptureBaseEditor.ResolutionStrings);
				}

				if (_renderResolution == CaptureBase.Resolution.Custom)
				{
					_renderSize = EditorGUILayout.Vector2Field("Size", _renderSize);
					_renderSize = new Vector2(Mathf.Clamp((int)_renderSize.x, 1, NativePlugin.MaxRenderWidth), Mathf.Clamp((int)_renderSize.y, 1, NativePlugin.MaxRenderHeight));
				}

				{
					string currentAA = "None";
					if (QualitySettings.antiAliasing > 1)
					{
						currentAA = QualitySettings.antiAliasing.ToString() + "x";
					}
					EditorUtils.IntAsDropdown("Anti-aliasing", _propRenderAntiAliasing, new string[] { "Current (" + currentAA + ")", "None", "2x", "4x", "8x" }, new int[] { -1, 1, 2, 4, 8 });
				}

				if (_cameraNode != null)
				{
					if (_cameraNode.actualRenderingPath == RenderingPath.DeferredLighting
#if AVPRO_MOVIECAPTURE_DEFERREDSHADING
					|| _cameraNode.actualRenderingPath == RenderingPath.DeferredShading
#endif
					)
					{
						GUI.color = Color.yellow;
						GUILayout.TextArea("Warning: Antialiasing by MSAA is not supported as camera is using deferred rendering path");
						GUI.color = Color.white;
						_renderAntiAliasing = -1;
					}
					if (_cameraNode.clearFlags == CameraClearFlags.Nothing || _cameraNode.clearFlags == CameraClearFlags.Depth)
					{
						if (_renderResolution != CaptureBase.Resolution.Original || _renderAntiAliasing != -1)
						{
							GUI.color = Color.yellow;
							GUILayout.TextArea("Warning: Overriding camera resolution or anti-aliasing when clear flag is set to " + _cameraNode.clearFlags + " may result in incorrect captures");
							GUI.color = Color.white;
						}
					}
				}

				EditorGUI.indentLevel--;
			}

			// 360 Cubemap
			if (_sourceType == SourceType.Camera360)
			{
				GUILayout.Space(8f);
				EditorGUILayout.LabelField("360 Camera", EditorStyles.boldLabel);
				EditorGUI.indentLevel++;
				EditorGUILayout.PropertyField(_propRender180Degrees);
				{
					CaptureBase.CubemapResolution cubemapEnum = (CaptureBase.CubemapResolution)_cubemapResolution;
					_cubemapResolution = (int)((CaptureBase.CubemapResolution)EditorGUILayout.EnumPopup("Resolution", cubemapEnum));
				}
				{
					CaptureBase.CubemapDepth depthEnum = (CaptureBase.CubemapDepth)_cubemapDepth;
					_cubemapDepth = (int)((CaptureBase.CubemapDepth)EditorGUILayout.EnumPopup("Depth", depthEnum));
				}
				{
					StereoPacking stereoEnum = (StereoPacking)_cubemapStereoPacking;
					_cubemapStereoPacking = (int)((StereoPacking)EditorGUILayout.EnumPopup("Stereo Mode", stereoEnum));
				}
				if (_cubemapStereoPacking != (int)StereoPacking.None)
				{
					#if AVPRO_MOVIECAPTURE_UNITY_STEREOCUBEMAP_RENDER
					if (!PlayerSettings.enable360StereoCapture)
					{
						GUI.color = Color.yellow;
						GUILayout.TextArea("Warning: 360 Stereo Capture needs to be enabled in PlayerSettings");
						GUI.color = Color.white;
						if (GUILayout.Button("Enable 360 Stereo Capture"))
						{
							PlayerSettings.enable360StereoCapture = true;
						}
					}
					#endif
					_cubemapStereoIPD = EditorGUILayout.FloatField("Interpupillary distance", _cubemapStereoIPD);
				}
				EditorGUILayout.PropertyField(_propCaptureWorldSpaceGUI, _guiCaptureWorldSpaceUI);
				EditorGUILayout.PropertyField(_propSupportCameraRotation, _guiCameraRotation);

				if (_propSupportCameraRotation.boolValue)
				{
					EditorGUILayout.PropertyField(_propOnlyLeftRightRotation);
				}
				EditorGUI.indentLevel--;
			}

			// 360 Cubemap ODS
			if (_sourceType == SourceType.Camera360ODS)
			{
				GUILayout.Space(8f);
				EditorGUI.indentLevel++;
				EditorGUILayout.LabelField("Source Options", EditorStyles.boldLabel);
				EditorGUI.indentLevel++;
				{
					EditorGUILayout.PropertyField(_propOdsRender180Degrees);
					EditorGUILayout.PropertyField(_propOdsIPD, _guiInterpupillaryDistance);
					EditorGUILayout.PropertyField(_propOdsPixelSliceSize);
					EditorGUILayout.PropertyField(_propOdsPaddingSize);
					EditorGUILayout.PropertyField(_propOdsCameraClearMode);
					EditorGUILayout.PropertyField(_propOdsCameraClearColor);
				}
				EditorGUI.indentLevel--;
				EditorGUI.indentLevel--;
			}

			// Start / Stop
			{
				GUILayout.Space(8f);
				EditorGUILayout.LabelField("Start / Stop", EditorStyles.boldLabel);
				EditorGUI.indentLevel++;

				EditorGUILayout.PropertyField(_propStartDelay, _guiStartDelay);

				if ((StartDelayMode)_propStartDelay.enumValueIndex == StartDelayMode.RealSeconds ||
					(StartDelayMode)_propStartDelay.enumValueIndex == StartDelayMode.GameSeconds)
				{
					EditorGUILayout.PropertyField(_propStartDelaySeconds, _guiSeconds);
				}

				EditorGUILayout.Separator();

				_stopMode = (StopMode)EditorGUILayout.EnumPopup("Stop Mode", _stopMode);
				if (_stopMode == StopMode.FramesEncoded)
				{
					_stopFrames = EditorGUILayout.IntField("Frames", _stopFrames);
				}
				else if (_stopMode == StopMode.SecondsElapsed || _stopMode == StopMode.SecondsEncoded)
				{
					_stopSeconds = EditorGUILayout.FloatField("Seconds", _stopSeconds);
				}
				EditorGUI.indentLevel--;
			}

			GUILayout.Space(8f);
			if (GUILayout.Button("Reset All Settings"))
			{
				ResetSettings();
			}
			GUILayout.Space(4f);

			//EditorGUI.indentLevel--;
			EditorGUILayout.EndVertical();
		}

		private void DrawConfigGUI_Encoding()
		{
			//GUILayout.Label("Target", EditorStyles.boldLabel);
			EditorGUILayout.BeginVertical("box");
			//EditorGUI.indentLevel++;

			EditorUtils.EnumAsDropdown("Output Type", _propOutputType, EditorUtils.OutputTypeNames);

			GUILayout.Space(8f);
			if (_propOutputType.enumValueIndex == (int)CaptureBase.OutputType.VideoFile ||
				_propOutputType.enumValueIndex == (int)CaptureBase.OutputType.ImageSequence)
			{
				bool isImageSequence = (_propOutputType.enumValueIndex == (int)CaptureBase.OutputType.ImageSequence);

				if (isImageSequence)
				{
					EditorUtils.EnumAsDropdown("Format", _propImageSequenceFormat, Utils.GetNativeImageSequenceFormatNames());
					GUILayout.Space(8f);
				}

				// File path
				EditorGUILayout.LabelField("File Path", EditorStyles.boldLabel);
				EditorGUI.indentLevel++;
				_outputFolderIndex = EditorGUILayout.Popup("Relative to", _outputFolderIndex, _outputFolders);
				if (_outputFolderIndex != (int)CaptureBase.OutputPath.Absolute)
				{
					_outputFolderRelative = EditorGUILayout.TextField("SubFolder(s)", _outputFolderRelative);
				}
				else
				{
					EditorGUILayout.BeginHorizontal();
					_outputFolderAbsolute = EditorGUILayout.TextField("Path", _outputFolderAbsolute);
					if (GUILayout.Button(">", GUILayout.Width(22)))
					{
						_outputFolderAbsolute = EditorUtility.SaveFolderPanel("Select Folder To Store Video Captures", System.IO.Path.GetFullPath(System.IO.Path.Combine(Application.dataPath, "../")), "");
						EditorUtility.SetDirty(this);
					}
					EditorGUILayout.EndHorizontal();
				}
				EditorGUI.indentLevel--;

				GUILayout.Space(8f);

				// File name
				EditorGUILayout.LabelField("File Name", EditorStyles.boldLabel);
				EditorGUI.indentLevel++;
				_filenamePrefixFromSceneName = EditorGUILayout.Toggle("From Scene Name", _filenamePrefixFromSceneName);
				if (_filenamePrefixFromSceneName)
				{
#if AVPRO_MOVIECAPTURE_SCENEMANAGER_53
					string currentScenePath = UnityEditor.SceneManagement.EditorSceneManager.GetActiveScene().path;
#else
					string currentScenePath = EditorApplication.currentScene;
#endif
					_filenamePrefix = System.IO.Path.GetFileNameWithoutExtension(currentScenePath);
					if (string.IsNullOrEmpty(_filenamePrefix))
					{
						_filenamePrefix = "capture";
					}
				}
				EditorGUI.BeginDisabledGroup(_filenamePrefixFromSceneName);
				_filenamePrefix = EditorGUILayout.TextField("Prefix", _filenamePrefix);
				EditorGUI.EndDisabledGroup();
				if (!isImageSequence)
				{
					_appendTimestamp = EditorGUILayout.Toggle("Append Timestamp", _appendTimestamp);
				}
				else
				{
					EditorGUILayout.PropertyField(_propImageSequenceStartFrame, _guiStartFrame);
					EditorGUILayout.PropertyField(_propImageSequenceZeroDigits, _guiZeroDigits);
				}
				EditorGUI.indentLevel--;
				GUILayout.Space(8f);

				// File container
				if (!isImageSequence)
				{
					EditorGUILayout.LabelField("File Container", EditorStyles.boldLabel);
					EditorGUI.indentLevel++;
					_fileContainerIndex = EditorGUILayout.Popup("Extension", _fileContainerIndex, _fileExtensions);
					_filenameExtension = _fileExtensions[_fileContainerIndex].ToLower();
					EditorGUI.indentLevel--;
				}
			}
			else if (_propOutputType.enumValueIndex == (int)CaptureBase.OutputType.NamedPipe)
			{
				EditorGUILayout.PropertyField(_propNamedPipePath);
			}

			DrawVisualCodecList();
			DrawAudioCodecList();

#if UNITY_EDITOR_WIN
			if (_propOutputType.enumValueIndex == (int)CaptureBase.OutputType.VideoFile)
			{
				if (_useMediaFoundationH264)
				{
					GUILayout.Space(8f);
					EditorGUILayout.LabelField("Post Capture Operations", EditorStyles.boldLabel);
					EditorGUI.indentLevel++;
					if (_propPostFastStartMp4 != null)
					{
						EditorGUILayout.PropertyField(_propPostFastStartMp4, _guiStreamableMP4);
					}
					EditorGUI.indentLevel--;
				}
			}
#endif

			//EditorGUI.indentLevel--;
			EditorGUILayout.EndVertical();
		}

		private void DrawConfigGUI_Visual()
		{
			//GUILayout.Label("Video", EditorStyles.boldLabel);
			EditorGUILayout.BeginVertical("box");
			//EditorGUI.indentLevel++;

			{
				Vector2 outSize = Vector2.zero;
				if (_sourceType == SourceType.Screen)
				{
					// We can't just use Screen.width and Screen.height because Unity returns the size of this window
					// So instead we look for a camera with no texture target and a valid viewport
					int inWidth = 1;
					int inHeight = 1;
					foreach (Camera cam in Camera.allCameras)
					{
						if (cam.targetTexture == null)
						{
							float rectWidth = Mathf.Clamp01(cam.rect.width + cam.rect.x) - Mathf.Clamp01(cam.rect.x);
							float rectHeight = Mathf.Clamp01(cam.rect.height + cam.rect.y) - Mathf.Clamp01(cam.rect.y);
							if (rectWidth > 0.0f && rectHeight > 0.0f)
							{
								inWidth = Mathf.FloorToInt(cam.pixelWidth / rectWidth);
								inHeight = Mathf.FloorToInt(cam.pixelHeight / rectHeight);
								//Debug.Log (rectWidth + "    " + (cam.rect.height - cam.rect.y) + " " + cam.pixelHeight + " = " + inWidth + "x" + inHeight);
								break;
							}
						}
					}
					outSize = CaptureBase.GetRecordingResolution(inWidth, inHeight, GetDownScaleFromIndex(_downScaleIndex), new Vector2(_downscaleX, _downscaleY));
				}
				else
				{
					if (_cameraNode != null)
					{
						int inWidth = Mathf.FloorToInt(_cameraNode.pixelRect.width);
						int inHeight = Mathf.FloorToInt(_cameraNode.pixelRect.height);

						if (_renderResolution != CaptureBase.Resolution.Original)
						{
							float rectWidth = Mathf.Clamp01(_cameraNode.rect.width + _cameraNode.rect.x) - Mathf.Clamp01(_cameraNode.rect.x);
							float rectHeight = Mathf.Clamp01(_cameraNode.rect.height + _cameraNode.rect.y) - Mathf.Clamp01(_cameraNode.rect.y);

							if (_renderResolution == CaptureBase.Resolution.Custom)
							{
								inWidth = (int)_renderSize.x;
								inHeight = (int)_renderSize.y;
							}
							else
							{
								CaptureBase.GetResolution(_renderResolution, ref inWidth, ref inHeight);
								inWidth = Mathf.FloorToInt(inWidth * rectWidth);
								inHeight = Mathf.FloorToInt(inHeight * rectHeight);
							}
						}

						outSize = CaptureBase.GetRecordingResolution(inWidth, inHeight, GetDownScaleFromIndex(_downScaleIndex), new Vector2(_downscaleX, _downscaleY));
					}
				}

				GUILayout.Space(8f);
				GUILayout.BeginHorizontal();
				GUILayout.FlexibleSpace();
				GUI.color = Color.cyan;
				GUILayout.TextArea("Output: " + (int)outSize.x + " x " + (int)outSize.y + " @ " + _frameRate.ToString("F2"));
				GUILayout.FlexibleSpace();
				GUILayout.EndHorizontal();
				GUILayout.Space(8f);
				GUI.color = Color.white;

			}

			_downScaleIndex = EditorGUILayout.Popup("Down Scale", _downScaleIndex, _downScales);
			if (_downScaleIndex == 5)
			{
				Vector2 maxVideoSize = new Vector2(_downscaleX, _downscaleY);
				maxVideoSize = EditorGUILayout.Vector2Field("Size", maxVideoSize);
				_downscaleX = Mathf.Clamp((int)maxVideoSize.x, 1, NativePlugin.MaxRenderWidth);
				_downscaleY = Mathf.Clamp((int)maxVideoSize.y, 1, NativePlugin.MaxRenderHeight);
			}

			_supportAlpha = EditorGUILayout.Toggle("Support Alpha", _supportAlpha);

			GUILayout.Space(8f);
			//EditorGUILayout.LabelField("Codec", EditorStyles.boldLabel);

			DrawConfigGUI_MotionBlur();

			//EditorGUI.indentLevel--;
			EditorGUILayout.EndVertical();
		}

		private void UpdateFileExtension()
		{
			_fileExtensions = GetSuitableFileExtensions(_videoCodecIndex, _audioCodecIndex);
			if (_fileContainerIndex >= _fileExtensions.Length)
			{
				_fileContainerIndex = 0;
			}
			if (_fileContainerIndex < _fileExtensions.Length)
			{
				_filenameExtension = _fileExtensions[_fileContainerIndex].ToLower();
			}
		}

		private void DrawVisualCodecList()
		{
			GUILayout.Space(8f);
			if (_outputType == CaptureBase.OutputType.VideoFile)
			{
				bool itemChanged = false;
				if (ShowConfigList("Video Codec", _videoCodecNames, _videoCodecConfigurable, ref _videoCodecIndex, ref itemChanged, true, true))
				{
#if UNITY_EDITOR_OSX
					_queueConfigureVideoCodec = Mathf.Max(-1, _videoCodecIndex);
#else
					_queueConfigureVideoCodec = Mathf.Max(-1, _videoCodecIndex - 4);
#endif
				}

			// Update file extensions based on selected codec
			if (itemChanged)
			{
				UpdateFileExtension();
			}

#if UNITY_EDITOR_WIN
				_useMediaFoundationH264 = (_videoCodecIndex == 2);

				// Display any warning messages based on codec selection
				if (_useMediaFoundationH264)
				{
					/*GUI.color = Color.yellow;
					GUILayout.TextArea("Warning: Make sure to set the file extension to .mp4");
					GUI.color = Color.white;*/
				}
				else
				{
					if (_videoCodecIndex > 0 && (
							_videoCodecNames[_videoCodecIndex].EndsWith("Cinepak Codec by Radius")
							|| _videoCodecNames[_videoCodecIndex].EndsWith("DV Video Encoder")
							|| _videoCodecNames[_videoCodecIndex].EndsWith("Microsoft Video 1")
							|| _videoCodecNames[_videoCodecIndex].EndsWith("Microsoft RLE")
							|| _videoCodecNames[_videoCodecIndex].EndsWith("Logitech Video (I420)")
							|| _videoCodecNames[_videoCodecIndex].EndsWith("Intel IYUV codec")
							))
					{
						GUI.color = Color.yellow;
						GUILayout.TextArea("Warning: Legacy codec, not recommended");
						GUI.color = Color.white;
					}
					if (_videoCodecIndex >= 0 &&
						(_videoCodecNames[_videoCodecIndex].Contains("Decoder") || _videoCodecNames[_videoCodecIndex].Contains("Decompressor")))
					{
						GUI.color = Color.yellow;
						GUILayout.TextArea("Warning: Codec may contain decompressor only");
						GUI.color = Color.white;
					}

					if (_videoCodecIndex >= 0 && _videoCodecNames[_videoCodecIndex].EndsWith("Uncompressed"))
					{
						GUI.color = Color.yellow;
						GUILayout.TextArea("Warning: Uncompressed may result in very large files");
						GUI.color = Color.white;
					}
					if (_videoCodecNames.Length < 8)
					{
						GUI.color = Color.cyan;
						GUILayout.TextArea("Low number of codecs, consider installing more");
						GUI.color = Color.white;
					}
				}
#else
				if (_videoCodecIndex >= 0 && _videoCodecNames[_videoCodecIndex].EndsWith("Uncompressed"))
				{
					GUI.color = Color.yellow;
					GUILayout.TextArea("Warning: Uncompressed may result in very large files");
					GUI.color = Color.white;
				}
#endif
			}
			/*else
			{
				GUI.color = Color.yellow;
				GUILayout.TextArea("Codec selection only available when using video file output");
				GUI.color = Color.white;
			}*/
		}

		private void DrawAudioCodecList()
		{
			if (_outputType != CaptureBase.OutputType.VideoFile)
			{
				return;
			}

			GUILayout.Space(8f);
			EditorGUI.BeginDisabledGroup(!_captureAudio);
			bool itemChanged = false;

#if UNITY_EDITOR_WIN
			// When using MF H.264 codec, we always just use AAC, so no need to show audio codec options
			if (_videoCodecIndex == 2)
			{
				int dummyAudioCodecIndex = 0;
				if (ShowConfigList("Audio Codec", new string[] { "AAC" }, new bool[] { false }, ref dummyAudioCodecIndex, ref itemChanged))
				{
				}
				EditorGUI.EndDisabledGroup();
				return;
			}
#endif

			if (ShowConfigList("Audio Codec", _audioCodecNames, _audioCodecConfigurable, ref _audioCodecIndex, ref itemChanged))
			{
#if UNITY_EDITOR_OSX
				_queueConfigureAudioCodec = Mathf.Max(-1, _audioCodecIndex);
#else
				_queueConfigureAudioCodec = Mathf.Max(-1, _audioCodecIndex - 2);
#endif
			}

			// Update file extensions based on selected codec
			if (itemChanged)
			{
				UpdateFileExtension();
			}

#if UNITY_EDITOR_WIN
			if (_audioCodecIndex > 0 && (_audioCodecNames[_audioCodecIndex].EndsWith("MPEG Layer-3")))
			{
				GUI.color = Color.yellow;
				GUILayout.TextArea("Warning: We have had reports that this codec doesn't work. Consider using a different codec");
				GUI.color = Color.white;
			}
#endif
			EditorGUI.EndDisabledGroup();
		}

		private void DrawConfigGUI_MotionBlur()
		{
			EditorGUI.BeginDisabledGroup(_captureModeIndex == 0);
			//EditorGUILayout.BeginVertical("box");
			//EditorGUI.indentLevel++;

			GUILayout.Space(8f);
			GUILayout.Label("Motion Blur (beta)", EditorStyles.boldLabel);
			//EditorGUILayout.BeginVertical("box");
			//EditorGUI.indentLevel++;

			if (_captureModeIndex == 0)
			{
				GUI.color = Color.yellow;
				GUILayout.TextArea("Motion Blur only available in Offline Render mode");
				GUI.color = Color.white;
			}

			_useMotionBlur = EditorGUILayout.Toggle("Use Motion Blur", _useMotionBlur);
			EditorGUI.BeginDisabledGroup(!_useMotionBlur);
			EditorGUILayout.PrefixLabel("Samples");
			EditorGUILayout.BeginHorizontal(GUILayout.ExpandWidth(false));
			//EditorGUILayout.LabelField("moo", GUILayout.ExpandWidth(false));
			_motionBlurSampleCount = EditorGUILayout.IntSlider(_motionBlurSampleCount, 0, 64);
			EditorGUILayout.EndHorizontal();
			EditorGUI.EndDisabledGroup();

			//EditorGUI.indentLevel--;
			//EditorGUILayout.EndVertical();
			EditorGUI.EndDisabledGroup();
		}

		private void DrawConfigGUI_Audio()
		{
			EditorGUI.BeginDisabledGroup(_captureModeIndex != 0 || _outputType != CaptureBase.OutputType.VideoFile);
			//GUILayout.Label("Audio", EditorStyles.boldLabel);
			EditorGUILayout.BeginVertical("box");
			//EditorGUI.indentLevel++;

			if (_captureModeIndex != 0)
			{
				GUI.color = Color.yellow;
				GUILayout.TextArea("Audio capture not available in Offline Render mode");
				GUI.color = Color.white;
			}
			if (_outputType != CaptureBase.OutputType.VideoFile)
			{
				GUI.color = Color.yellow;
				GUILayout.TextArea("Audio capture only available when outputing to video file");
				GUI.color = Color.white;
			}

			_captureAudio = EditorGUILayout.Toggle("Capture Audio", _captureAudio);

			GUILayout.Space(8f);
			EditorGUI.BeginDisabledGroup(!_captureAudio);
			bool itemChanged = false;
			if (ShowConfigList("Source", _audioDeviceNames, null, ref _audioDeviceIndex, ref itemChanged, false))
			{
			}

			GUILayout.Space(8f);

			EditorGUI.EndDisabledGroup();

			//EditorGUI.indentLevel--;
			EditorGUILayout.EndVertical();
			EditorGUI.EndDisabledGroup();
		}

		private static string[] GetSuitableFileExtensions(int videoCodecIndex, int audioCodecIndex)
		{
			string[] result;

#if UNITY_EDITOR_OSX
			result = NativePlugin.GetContainerFileExtensions(videoCodecIndex, audioCodecIndex);
#elif UNITY_EDITOR_WIN
			if (videoCodecIndex == 2)
			{
				result = new string[] { "MP4" };
			}
			else
			{
				result = new string[] { "AVI" };
			}
#else
			result = new string[0];
#endif
			for (int i = 0; i < result.Length; i++)
			{
				result[i] = result[i].ToUpper();
			}
			return result;
		}

		private static CaptureBase.DownScale GetDownScaleFromIndex(int index)
		{
			CaptureBase.DownScale result = CaptureBase.DownScale.Original;
			switch (index)
			{
				case 0:
					result = CaptureBase.DownScale.Original;
					break;
				case 1:
					result = CaptureBase.DownScale.Half;
					break;
				case 2:
					result = CaptureBase.DownScale.Quarter;
					break;
				case 3:
					result = CaptureBase.DownScale.Eighth;
					break;
				case 4:
					result = CaptureBase.DownScale.Sixteenth;
					break;
				case 5:
					result = CaptureBase.DownScale.Custom;
					break;
			}

			return result;
		}

		private static bool IsTrialVersion()
		{
			return NativePlugin.IsTrialVersion();
		}
	}
}
#endif