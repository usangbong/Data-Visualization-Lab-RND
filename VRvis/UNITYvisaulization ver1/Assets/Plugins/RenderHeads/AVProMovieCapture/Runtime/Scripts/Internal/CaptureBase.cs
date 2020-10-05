#if UNITY_5_4_OR_NEWER || (UNITY_5 && !UNITY_5_0 && !UNITY_5_1)
	#define AVPRO_MOVIECAPTURE_GLISSUEEVENT_52
#endif
#if UNITY_5_4_OR_NEWER || UNITY_5
	#define AVPRO_MOVIECAPTURE_DEFERREDSHADING
#endif
#if UNITY_2017_1_OR_NEWER
	#define AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
#endif
#if UNITY_2019_2_OR_NEWER
	#define AVPRO_MOVIECAPTURE_CAPTUREDELTA_SUPPORT
#endif
#if ENABLE_IL2CPP
using AOT;
#endif
using UnityEngine;
using System.IO;
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;

//-----------------------------------------------------------------------------
// Copyright 2012-2020 RenderHeads Ltd.  All rights reserved.
//-----------------------------------------------------------------------------

namespace RenderHeads.Media.AVProMovieCapture
{
	/// <summary>
	/// Base class wrapping common capture functionality
	/// </summary>
	public class CaptureBase : MonoBehaviour
	{
		public enum Resolution
		{
			POW2_8192x8192,
			POW2_8192x4096,
			POW2_4096x4096,
			POW2_4096x2048,
			POW2_2048x4096,
			UHD_3840x2160,
			UHD_3840x2048,
			UHD_3840x1920,
			POW2_2048x2048,
			POW2_2048x1024,
			HD_1920x1080,
			HD_1280x720,
			SD_1024x768,
			SD_800x600,
			SD_800x450,
			SD_640x480,
			SD_640x360,
			SD_320x240,
			Original,
			Custom,
		}

		public enum CubemapDepth
		{
			Depth_24 = 24,
			Depth_16 = 16,
			Depth_Zero = 0,
		}

		public enum CubemapResolution
		{
			POW2_4096 = 4096,
			POW2_2048 = 2048,
			POW2_1024 = 1024,
			POW2_512 = 512,
			POW2_256 = 256,
		}

		public enum AntiAliasingLevel
		{
			UseCurrent,
			ForceNone,
			ForceSample2,
			ForceSample4,
			ForceSample8,
		}

		public enum DownScale
		{
			Original = 1,
			Half = 2,
			Quarter = 4,
			Eighth = 8,
			Sixteenth = 16,
			Custom = 100,
		}

		public enum OutputPath
		{
			RelativeToProject,
			RelativeToPeristentData,
			Absolute,
			RelativeToDesktop,
		}

		/*public enum OutputExtension
		{
			AVI,
			MP4,
			PNG,
			Custom = 100,
		}*/

		public enum OutputType
		{
			VideoFile,
			ImageSequence,
			NamedPipe,
		}

		[System.Serializable]
		public class WindowsPostCaptureSettings
		{
			[SerializeField]
			[Tooltip("Move the 'moov' atom in the MP4 file from the end to the start of the file to make streaming start fast.  Also called 'Fast Start' in some encoders")]
			public bool writeFastStartStreamingForMp4 = true;
		}

		[System.Serializable]
		public class PostCaptureSettings
		{
			[SerializeField]
			[Tooltip("Move the 'moov' atom in the MP4 file from the end to the start of the file to make streaming start fast.  Also called 'Fast Start' in some encoders")]
			public WindowsPostCaptureSettings windows = new WindowsPostCaptureSettings();
		}

		[SerializeField]
		private PostCaptureSettings _postCaptureSettings = new PostCaptureSettings();

		// General options

		public KeyCode _captureKey = KeyCode.None;
		public bool _listVideoCodecsOnStart = false;
		public bool _isRealTime = true;

		[SerializeField]
		private bool _persistAcrossSceneLoads = false;

		// Start options

		[SerializeField]
		private StartTriggerMode _startTrigger = StartTriggerMode.Manual;

		[SerializeField]
		private StartDelayMode _startDelay = StartDelayMode.None;

		[SerializeField]
		private float _startDelaySeconds = 0f;

		// Stop options

		public StopMode _stopMode = StopMode.None;
		// TODO: add option to pause instread of stop?
		public int _stopFrames = 0;
		public float _stopSeconds = 0f;

		// Video options

		public bool _useMediaFoundationH264 = true;

		[SerializeField]
		private string[] _videoCodecPriorityWindows = { "Lagarith Lossless Codec",
														"x264vfw - H.264/MPEG-4 AVC codec",
														"Xvid MPEG-4 Codec" };

		[SerializeField]
		private string[] _videoCodecPriorityMacOS = {	"H264",
														"HEVC",
														"Apple ProRes 422",
														"Apple ProRes 4444" };

		[SerializeField] float _frameRate = 30f;

		[SerializeField]
		[Tooltip("Timelapse scale makes the frame capture run at a fraction of the target frame rate.  Default value is 1")]
		private int _timelapseScale = 1;
		public DownScale _downScale = DownScale.Original;
		public Vector2 _maxVideoSize = Vector2.zero;
		#pragma warning disable 414
		[SerializeField] int _forceVideoCodecIndexWindows = -1;
		[SerializeField] int _forceVideoCodecIndexMacOS = 0;
		[SerializeField] int _forceVideoCodecIndexIOS = 0;
		#pragma warning restore 414
		public bool _flipVertically = false;
		public bool _supportAlpha = false;

		[Tooltip("Flushing the GPU during each capture results in less latency, but can slow down rendering performance for complex scenes.")]
		[SerializeField]
		private bool _forceGpuFlush = false;

		[Tooltip("This option can help issues where skinning is used, or other animation/rendering effects that only complete later in the frame.")]
		[SerializeField]
		protected bool _useWaitForEndOfFrame = true;

		// Audio options

		public bool _noAudio = true;
		public string[] _audioCodecPriority = { };
		public int _forceAudioCodecIndex = -1;
		public int _forceAudioDeviceIndex = -1;
		public UnityAudioCapture _audioCapture;

		// Output options
#if (!UNITY_EDITOR && UNITY_IOS)
		// Can only write to persistent data path (Documents) on iOS
		public OutputPath _outputFolderType = OutputPath.RelativeToPeristentData;
		// Subfolders prevent direct access via iTunes so avoid
		public string _outputFolderPath = "";
#else
		public OutputPath _outputFolderType = OutputPath.RelativeToProject;
		public string _outputFolderPath = "Captures";
#endif
		public bool _appendFilenameTimestamp = true;
		public string _filenamePrefix = "MovieCapture";
		public bool _allowManualFileExtension = false;
#if UNITY_EDITOR_WIN || (!UNITY_EDITOR && UNITY_STANDALONE_WIN)
		public string _filenameExtension = "avi";
#else
		public string _filenameExtension = "mp4";
#endif
		public string _namedPipePath = @"\\.\pipe\test_pipe";

		public int _imageSequenceStartFrame = 0;
		[Range(2, 12)]
		public int _imageSequenceZeroDigits = 6;
		public OutputType _outputType = OutputType.VideoFile;
		public ImageSequenceFormat _imageSequenceFormatWindows = ImageSequenceFormat.PNG;
		public ImageSequenceFormat _imageSequenceFormatMacOS = ImageSequenceFormat.PNG;
		public ImageSequenceFormat _imageSequenceFormatIOS = ImageSequenceFormat.PNG;

		// Camera specific options

		public Resolution _renderResolution = Resolution.Original;
		public Vector2 _renderSize = Vector2.one;
		public int _renderAntiAliasing = -1;

		// Motion blur options

		public bool _useMotionBlur = false;
		[Range(0, 64)]
		public int _motionBlurSamples = 16;
		public Camera[] _motionBlurCameras = null;
		protected MotionBlur _motionBlur;

		// Performance options

		public bool _allowVSyncDisable = true;

		[SerializeField]
		protected bool _supportTextureRecreate = false;

#if AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
		[SerializeField] TimelineController _timelineController = null;
#endif

		//public bool _allowFrameRateChange = true;

		// Cursor options
		public bool _captureMouseCursor = false;
		public MouseCursor _mouseCursor;

		[System.NonSerialized]
		public string _codecName = "uncompressed";
		[System.NonSerialized]
		public int _codecIndex = -1;

		[System.NonSerialized]
		public string _audioCodecName = "uncompressed";
		[System.NonSerialized]
		public int _audioCodecIndex = -1;

		[System.NonSerialized]
		public string _audioDeviceName = "Unity";
		[System.NonSerialized]
		public int _audioDeviceIndex = -1;

		[System.NonSerialized]
		public int _unityAudioSampleRate = -1;
		[System.NonSerialized]
		public int _unityAudioChannelCount = -1;

		protected Texture2D _texture;
		protected int _handle = -1;
		protected int _targetWidth, _targetHeight;
		protected bool _capturing = false;
		protected bool _paused = false;
		protected string _filePath;
		protected FileInfo _fileInfo;
		protected NativePlugin.PixelFormat _pixelFormat = NativePlugin.PixelFormat.YCbCr422_YUY2;
		private int _oldVSyncCount = 0;
		//private int _oldTargetFrameRate = -1;
		private float _oldFixedDeltaTime = 0f;
		protected bool _isTopDown = true;
		protected bool _isDirectX11 = false;
		private bool _queuedStartCapture = false;
		private bool _queuedStopCapture = false;
		private float _captureStartTime = 0f;
		private float _timeSinceLastFrame = 0f;
		protected YieldInstruction _waitForEndOfFrame;

		private float _startDelayTimer;
		private bool _startPaused;
		private System.Action<FileWritingHandler> _fileWritingAction;
		private List<FileWritingHandler> _pendingFileWrites = new List<FileWritingHandler>(4);

		public string LastFilePath
		{
			get { return _filePath; }
		}

		public System.Action<FileWritingHandler> FileWritingAction
		{
			get { return _fileWritingAction; }
			set { _fileWritingAction = value; }
		}

		// Other options
		public int _minimumDiskSpaceMB = -1;
		private long _freeDiskSpaceMB;

		// Stats
		private uint _numDroppedFrames;
		private uint _numDroppedEncoderFrames;
		private uint _numEncodedFrames;
		private uint _totalEncodedSeconds;

		private static bool _isInitialised = false;

#if AVPRO_MOVIECAPTURE_GLISSUEEVENT_52
		protected System.IntPtr _renderEventFunction = System.IntPtr.Zero;
		protected System.IntPtr _freeEventFunction = System.IntPtr.Zero;
#endif

		public float FrameRate
		{
			get { return _frameRate; }
			set { _frameRate = Mathf.Clamp(value, 0.01f, 240f); }
		}

		public StartTriggerMode StartTrigger
		{
			get { return _startTrigger; }
			set { _startTrigger = value; }
		}

		public StartDelayMode StartDelay
		{
			get { return _startDelay; }
			set { _startDelay = value; }
		}

		public float StartDelaySeconds
		{
			get { return _startDelaySeconds; }
			set { _startDelaySeconds = value; }
		}

		public uint NumDroppedFrames
		{
			get { return _numDroppedFrames; }
		}

		public uint NumDroppedEncoderFrames
		{
			get { return _numDroppedEncoderFrames; }
		}

		public uint NumEncodedFrames
		{
			get { return _numEncodedFrames; }
		}

		public uint TotalEncodedSeconds
		{
			get { return _totalEncodedSeconds; }
		}

		public string[] VideoCodecPriorityWindows
		{
			get { return _videoCodecPriorityWindows; }
			set { _videoCodecPriorityWindows = value; SelectCodec(false); }
		}

		public string[] VideoCodecPriorityMacOS
		{
			get { return _videoCodecPriorityMacOS; }
			set { _videoCodecPriorityMacOS = value; SelectCodec(false); }
		}		

		public int TimelapseScale
		{
			get { return _timelapseScale; }
			set { _timelapseScale = value; }
		}

		public bool UseWaitForEndOfFrame
		{
			get { return _useWaitForEndOfFrame; }
			set { _useWaitForEndOfFrame = value; }
		}

		public PostCaptureSettings PostCapture
		{
			get { return _postCaptureSettings; }
		}

		#if AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
		public TimelineController TimelineController
		{
			get { return _timelineController; }
			set { _timelineController = value; }
		}
		#endif

		public int NativeForceVideoCodecIndex
		{
			#if UNITY_EDITOR
				#if UNITY_EDITOR_WIN
					get { return _forceVideoCodecIndexWindows; }
					set { _forceVideoCodecIndexWindows = value; }
				#elif UNITY_EDITOR_OSX
					get { return _forceVideoCodecIndexMacOS; }
					set { _forceVideoCodecIndexMacOS = value; }
				#else
					get { return _forceVideoCodecIndexWindows; }
					set { _forceVideoCodecIndexWindows = value; }
				#endif
			#else
				#if UNITY_STANDALONE_WIN
					get { return _forceVideoCodecIndexWindows; }
					set { _forceVideoCodecIndexWindows = value; }
				#elif UNITY_STANDALONE_OSX
					get { return _forceVideoCodecIndexMacOS; }
					set { _forceVideoCodecIndexMacOS = value; }
				#elif UNITY_IOS
					get { return _forceVideoCodecIndexIOS; }
					set { _forceVideoCodecIndexIOS = value; }
				#else
					get { return _imageSequenceFormatWindows; }
					set { _imageSequenceFormatWindows = value; }
				#endif
			#endif
		}

		public ImageSequenceFormat NativeImageSequenceFormat
		{
			#if UNITY_EDITOR
				#if UNITY_EDITOR_WIN
					get { return _imageSequenceFormatWindows; }
					set { _imageSequenceFormatWindows = value; }
				#elif UNITY_EDITOR_OSX
					get { return _imageSequenceFormatMacOS; }
					set { _imageSequenceFormatMacOS = value; }
				#else
					get { return _imageSequenceFormatWindows; }
					set { _imageSequenceFormatWindows = value; }
				#endif
			#else
				#if UNITY_STANDALONE_WIN
					get { return _imageSequenceFormatWindows; }
					set { _imageSequenceFormatWindows = value; }
				#elif UNITY_STANDALONE_OSX
					get { return _imageSequenceFormatMacOS; }
					set { _imageSequenceFormatMacOS = value; }
				#elif UNITY_IOS
					get { return _imageSequenceFormatIOS; }
					set { _imageSequenceFormatIOS = value; }
				#else
					get { return _imageSequenceFormatWindows; }
					set { _imageSequenceFormatWindows = value; }
				#endif
			#endif
		}

		protected virtual void Awake()
		{
			if (!_isInitialised)
			{
				try
				{
					string pluginVersionString = NativePlugin.GetPluginVersionString();

					// Check that the plugin version number is not too old
					if (!pluginVersionString.StartsWith(NativePlugin.ExpectedPluginVersion))
					{
						Debug.LogWarning("[AVProMovieCapture] Plugin version number " + pluginVersionString + " doesn't match the expected version number " + NativePlugin.ExpectedPluginVersion + ".  It looks like the plugin didn't upgrade correctly.  To resolve this please restart Unity and try to upgrade the package again.");
					}

		#if UNITY_EDITOR_OSX || UNITY_STANDALONE_OSX
			#if !UNITY_2017_1_OR_NEWER
					if (SystemInfo.graphicsDeviceVersion.StartsWith("Metal"))
					{
						Debug.LogError("[AVProMovieCapture] Metal is not supported below Unity 2017, please switch to OpenGLCore in Player Settings.");
						return;
					}
			#endif
		#elif !UNITY_EDITOR && UNITY_IOS && !UNITY_2017_1_OR_NEWER
					if (Application.isPlaying)
					{
						Debug.LogError("[AVProMovieCapture] iOS is not supported below Unity 2017.");
						return;
					}
		#endif
					if (NativePlugin.Init())
					{
						Debug.Log("[AVProMovieCapture] Init plugin version: " + pluginVersionString + " (script v" + NativePlugin.ScriptVersion +") with GPU " + SystemInfo.graphicsDeviceName + " " + SystemInfo.graphicsDeviceVersion + " OS: " + SystemInfo.operatingSystem);
						SetupRenderFunctions();
						_isInitialised = true;
					}
					else
					{
						Debug.LogError("[AVProMovieCapture] Failed to initialise plugin version: " + pluginVersionString + " (script v" + NativePlugin.ScriptVersion + ") with GPU " + SystemInfo.graphicsDeviceName + " " + SystemInfo.graphicsDeviceVersion + " OS: " + SystemInfo.operatingSystem);
					}
				}
				catch (DllNotFoundException e)
				{
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
			}
			else
			{
				SetupRenderFunctions();
			}

			_isDirectX11 = SystemInfo.graphicsDeviceVersion.StartsWith("Direct3D 11");

			SelectCodec(_listVideoCodecsOnStart);
			SelectAudioCodec(_listVideoCodecsOnStart);
			SelectAudioDevice(_listVideoCodecsOnStart);

			if (_persistAcrossSceneLoads)
			{
				GameObject.DontDestroyOnLoad(this.gameObject);
			}
		}

		protected void SetupRenderFunctions()
		{
			#if AVPRO_MOVIECAPTURE_GLISSUEEVENT_52
			_renderEventFunction = NativePlugin.GetRenderEventFunc();
			_freeEventFunction = NativePlugin.GetFreeResourcesEventFunc();
			Debug.Assert(_renderEventFunction != System.IntPtr.Zero);
			Debug.Assert(_freeEventFunction != System.IntPtr.Zero);
			#endif
		}

		public virtual void Start()
		{
			Application.runInBackground = true;
			_waitForEndOfFrame = new WaitForEndOfFrame();

			if (_startTrigger == StartTriggerMode.OnStart)
			{
				StartCapture();
			}
		}

		public void SelectCodec(bool listCodecs, bool isStartingCapture = false)
		{
			// Enumerate video codecs
			int numVideoCodecs = NativePlugin.GetNumAVIVideoCodecs();
			if (listCodecs)
			{
				for (int i = 0; i < numVideoCodecs; i++)
				{
					Debug.Log("VideoCodec " + i + ": " + NativePlugin.GetAVIVideoCodecName(i));
				}
			}
#if UNITY_EDITOR_WIN || (!UNITY_EDITOR && UNITY_STANDALONE_WIN)
			_codecIndex = -1;
			_codecName = "Uncompressed";

			if (_useMediaFoundationH264)
			{
				_codecName = "Media Foundation H.264(MP4)";
			}
			else
			{
				// The user has specified their own codec index
				if (NativeForceVideoCodecIndex >= 0)
				{
					if (NativeForceVideoCodecIndex < numVideoCodecs)
					{
						_codecName = NativePlugin.GetAVIVideoCodecName(NativeForceVideoCodecIndex);
						_codecIndex = NativeForceVideoCodecIndex;
					}

					if (_codecIndex < 0)
					{
						_codecName = "Uncompressed";
						if (isStartingCapture)
						{
							Debug.LogWarning("[AVProMovieCapture] Video codec not found.  Video will be uncompressed.");
						}
					}
				}
				else
				{
					// Try to find the codec based on the priority list
					if (_videoCodecPriorityWindows != null && _videoCodecPriorityWindows.Length > 0)
					{
						foreach (string codec in _videoCodecPriorityWindows)
						{
							string codecName = codec.Trim();
							// Empty string means uncompressed
							if (string.IsNullOrEmpty(codecName) || codecName == "Uncompressed")
							{
								_codecName = "Uncompressed";
								break;
							}

							for (int i = 0; i < numVideoCodecs; i++)
							{
								if (codecName == NativePlugin.GetAVIVideoCodecName(i))
								{
									_codecName = codecName;
									_codecIndex = i;
									break;
								}
							}

							if (_codecIndex >= 0)
								break;
						}

						if (_codecIndex < 0)
						{
							_codecName = "Uncompressed";
							if (isStartingCapture)
							{
								Debug.LogWarning("[AVProMovieCapture] Video codec not found.  Video will be uncompressed.");
							}
						}
					}
				}
			}
#else
			_codecIndex = 0;
			if (NativeForceVideoCodecIndex > _codecIndex)
			{
				// The user has specified their own codec index
				if (NativeForceVideoCodecIndex < numVideoCodecs)
				{
					_codecIndex = NativeForceVideoCodecIndex;
				}
			}
			else
			{
				#if UNITY_STANDALONE_OSX
				// Try to find the codec based on the priority list
				if (_videoCodecPriorityMacOS != null && _videoCodecPriorityMacOS.Length > 0)
				{
					foreach (string codec in _videoCodecPriorityMacOS)
					{
						string codecName = codec.Trim();
						if (!string.IsNullOrEmpty(codecName))
						{
							for (int i = 0; i < numVideoCodecs; i++)
							{
								if (codecName == NativePlugin.GetAVIVideoCodecName(i))
								{
									_codecName = codecName;
									_codecIndex = i;
									break;
								}
							}

							if (_codecIndex >= 0)
								break;
						}
					}
				}
				#endif
			}
			_codecName = NativePlugin.GetAVIVideoCodecName(_codecIndex);
#endif
		}

		public void SelectAudioCodec(bool listCodecs)
		{
			// Enumerate audio codecs
			int numAudioCodecs = NativePlugin.GetNumAVIAudioCodecs();
			if (listCodecs)
			{
				for (int i = 0; i < numAudioCodecs; i++)
				{
					Debug.Log("AudioCodec " + i + ": " + NativePlugin.GetAVIAudioCodecName(i));
				}
			}

#if UNITY_EDITOR_WIN || (!UNITY_EDITOR && UNITY_STANDALONE_WIN)
			_audioCodecIndex = -1;

			// The user has specified their own codec index
			if (_forceAudioCodecIndex >= 0)
			{
				if (_forceAudioCodecIndex < numAudioCodecs)
				{
					_audioCodecName = NativePlugin.GetAVIAudioCodecName(_forceAudioCodecIndex);
					_audioCodecIndex = _forceAudioCodecIndex;
				}

				if (_audioCodecIndex < 0)
				{
					_audioCodecName = "Uncompressed";
					Debug.LogWarning("[AVProMovieCapture] Audio codec not found.  Audio will be uncompressed.");
				}
			}
			else
			{
				// Try to find the codec based on the priority list
				if (_audioCodecPriority != null && _audioCodecPriority.Length > 0)
				{
					foreach (string codec in _audioCodecPriority)
					{
						string codecName = codec.Trim();
						// Empty string means uncompressed
						if (string.IsNullOrEmpty(codecName))
							break;

						for (int i = 0; i < numAudioCodecs; i++)
						{
							if (codecName == NativePlugin.GetAVIAudioCodecName(i))
							{
								_audioCodecName = codecName;
								_audioCodecIndex = i;
								break;
							}
						}

						if (_audioCodecIndex >= 0)
							break;
					}

					if (_audioCodecIndex < 0)
					{
						_audioCodecName = "Uncompressed";
						Debug.LogWarning("[AVProMovieCapture] Codec not found.  Audio will be uncompressed.");
					}
				}
			}
#else
			_audioCodecIndex = 0;
			if (_forceAudioCodecIndex >= 0)
			{
				if (_forceAudioCodecIndex < numAudioCodecs)
				{
					_audioCodecName = NativePlugin.GetAVIAudioCodecName(_forceAudioCodecIndex);
					_audioCodecIndex = _forceAudioCodecIndex;
				}
			}
			else
			{
				_audioCodecName = NativePlugin.GetAVIAudioCodecName(_audioCodecIndex);
			}
#endif
		}

		public void SelectAudioDevice(bool display)
		{
			// Enumerate
			int num = NativePlugin.GetNumAVIAudioInputDevices();
			if (display)
			{
				for (int i = 0; i < num; i++)
				{
					Debug.Log("AudioDevice " + i + ": " + NativePlugin.GetAVIAudioInputDeviceName(i));
				}
			}

			// The user has specified their own device index
			if (_forceAudioDeviceIndex >= 0)
			{
				if (_forceAudioDeviceIndex < num)
				{
					_audioDeviceName = NativePlugin.GetAVIAudioInputDeviceName(_forceAudioDeviceIndex);
					_audioDeviceIndex = _forceAudioDeviceIndex;
				}
			}
			else
			{
				/*_audioDeviceIndex = -1;
				// Try to find one of the loopback devices
				for (int i = 0; i < num; i++)
				{
					StringBuilder sbName = new StringBuilder(512);
					if (AVProMovieCapturePlugin.GetAVIAudioInputDeviceName(i, sbName))
					{
						string[] loopbackNames = { "Stereo Mix", "What U Hear", "What You Hear", "Waveout Mix", "Mixed Output" };
						for (int j = 0; j < loopbackNames.Length; j++)
						{
							if (sbName.ToString().Contains(loopbackNames[j]))
							{
								_audioDeviceIndex = i;
								_audioDeviceName = sbName.ToString();
							}
						}
					}
					if (_audioDeviceIndex >= 0)
						break;
				}

				if (_audioDeviceIndex < 0)
				{
					// Resort to the no recording device
					_audioDeviceName = "Unity";
					_audioDeviceIndex = -1;
				}*/

				_audioDeviceName = "Unity";
				_audioDeviceIndex = -1;
			}
		}

		public static Vector2 GetRecordingResolution(int width, int height, DownScale downscale, Vector2 maxVideoSize)
		{
			int targetWidth = width;
			int targetHeight = height;
			if (downscale != DownScale.Custom)
			{
				targetWidth /= (int)downscale;
				targetHeight /= (int)downscale;
			}
			else
			{
				if (maxVideoSize.x >= 1.0f && maxVideoSize.y >= 1.0f)
				{
					targetWidth = Mathf.FloorToInt(maxVideoSize.x);
					targetHeight = Mathf.FloorToInt(maxVideoSize.y);
				}
			}

			// Some codecs like Lagarith in YUY2 mode need size to be multiple of 4
			targetWidth = NextMultipleOf4(targetWidth);
			targetHeight = NextMultipleOf4(targetHeight);

			return new Vector2(targetWidth, targetHeight);
		}

		public void SelectRecordingResolution(int width, int height)
		{
			_targetWidth = width;
			_targetHeight = height;
			if (_downScale != DownScale.Custom)
			{
				_targetWidth /= (int)_downScale;
				_targetHeight /= (int)_downScale;
			}
			else
			{
				if (_maxVideoSize.x >= 1.0f && _maxVideoSize.y >= 1.0f)
				{
					_targetWidth = Mathf.FloorToInt(_maxVideoSize.x);
					_targetHeight = Mathf.FloorToInt(_maxVideoSize.y);
				}
			}

			// Some codecs like Lagarith in YUY2 mode need size to be multiple of 4
			_targetWidth = NextMultipleOf4(_targetWidth);
			_targetHeight = NextMultipleOf4(_targetHeight);
		}

		public virtual void OnDestroy()
		{
			_waitForEndOfFrame = null;
			StopCapture(false, true);
			FreePendingFileWrites();
		}

		private void FreePendingFileWrites()
		{
			foreach (FileWritingHandler handler in _pendingFileWrites)
			{
				handler.Dispose();
			}
			_pendingFileWrites.Clear();
		}

		private void OnApplicationQuit()
		{
			StopCapture(false, true);
			if (_isInitialised)
			{
				NativePlugin.Deinit();
				_isInitialised = false;
			}
		}

		protected void EncodeTexture(Texture2D texture)
		{
			Color32[] bytes = texture.GetPixels32();
			GCHandle _frameHandle = GCHandle.Alloc(bytes, GCHandleType.Pinned);

			EncodePointer(_frameHandle.AddrOfPinnedObject());

			if (_frameHandle.IsAllocated)
			{
				_frameHandle.Free();
			}
		}

		protected bool IsUsingUnityAudio()
		{
			return (_isRealTime && _outputType == OutputType.VideoFile && !_noAudio && _audioDeviceIndex < 0 && _audioCapture != null);
		}

		protected bool IsRecordingUnityAudio()
		{
			return (IsUsingUnityAudio() && _audioCapture.isActiveAndEnabled);
		}

		protected bool IsUsingMotionBlur()
		{
			return (_useMotionBlur && !_isRealTime && _motionBlur != null);
		}

		public virtual void EncodePointer(System.IntPtr ptr)
		{
			if (!IsRecordingUnityAudio())
			{
				NativePlugin.EncodeFrame(_handle, ptr);
			}
			else
			{
				int audioDataLength = 0;
				System.IntPtr audioDataPtr = _audioCapture.ReadData(out audioDataLength);
				if (audioDataLength > 0)
				{
					NativePlugin.EncodeFrameWithAudio(_handle, ptr, audioDataPtr, (uint)audioDataLength);
				}
				else
				{
					NativePlugin.EncodeFrame(_handle, ptr);
				}
			}
		}

		public bool IsCapturing()
		{
			return _capturing;
		}

		public bool IsPaused()
		{
			return _paused;
		}

		public int GetRecordingWidth()
		{
			return _targetWidth;
		}

		public int GetRecordingHeight()
		{
			return _targetHeight;
		}

		protected virtual string GenerateTimestampedFilename(string filenamePrefix, string filenameExtension)
		{
			// TimeSpan span = (DateTime.Now - DateTime.Now.Date);
			// string filename = string.Format("{0}-{1}-{2}-{3}-{4}s-{5}x{6}", filenamePrefix, DateTime.Now.Year, DateTime.Now.Month.ToString("D2"), DateTime.Now.Day.ToString("D2"), ((int)(span.TotalSeconds)).ToString(), _targetWidth, _targetHeight);
			// [MOZ] Use actual time in place of seconds
			string dateTime = DateTime.Now.ToString("yyyy-MM-dd_HH-mm-ss");
			string filename = string.Format("{0}_{1}_{2}x{3}", filenamePrefix, dateTime, _targetWidth, _targetHeight);
			// [MOZ] File extension is now optional
			if (filenameExtension != null) {
				filename = filename + "." + filenameExtension;
			}
			return filename;
		}

		private static string GetFolder(OutputPath outputPathType, string path)
		{
#if !UNITY_EDITOR && UNITY_IOS
			if (outputPathType != OutputPath.RelativeToPeristentData)
			{
				Debug.LogWarning("Only OutputPath.RelativeToPeristentData is supported on iOS");
				outputPathType = OutputPath.RelativeToPeristentData;
			}
			if (path.Length > 0)
			{
				Debug.LogWarning("Subfolders not supported on iOS");
				path = "";
			}
#endif
			string fileFolder = string.Empty;
			if (outputPathType == OutputPath.RelativeToProject)
			{
				string projectFolder = System.IO.Path.GetFullPath(System.IO.Path.Combine(Application.dataPath, ".."));
				fileFolder = System.IO.Path.Combine(projectFolder, path);
			}
			else if (outputPathType == OutputPath.RelativeToPeristentData)
			{
				string dataFolder = System.IO.Path.GetFullPath(Application.persistentDataPath);
				fileFolder = System.IO.Path.Combine(dataFolder, path);
			}
			else if (outputPathType == OutputPath.RelativeToDesktop)
			{
				string desktopFolder = System.Environment.GetFolderPath(System.Environment.SpecialFolder.DesktopDirectory);
				fileFolder = System.IO.Path.Combine(desktopFolder, path);
			}
			else if (outputPathType == OutputPath.Absolute)
			{
				fileFolder = path;
			}
			return fileFolder;
		}

		private static string GenerateFilePath(OutputPath outputPathType, string path, string filename)
		{
			// Resolve folder
			string fileFolder = GetFolder(outputPathType, path);

			// Combine path and filename
			return System.IO.Path.Combine(fileFolder, filename);
		}

		protected static bool HasExtension(string path, string extension)
		{
			return path.ToLower().EndsWith(extension, StringComparison.OrdinalIgnoreCase);
		}

		protected void GenerateFilename()
		{
			string filename = string.Empty;
			if (_outputType == OutputType.VideoFile)
			{
				if (!_allowManualFileExtension)
				{
#if UNITY_EDITOR_WIN || (!UNITY_EDITOR && UNITY_STANDALONE_WIN)
					_filenameExtension = "avi";
					if (_useMediaFoundationH264)
					{
						_filenameExtension = "mp4";
					}
#elif UNITY_EDITOR_OSX || (!UNITY_EDITOR && (UNITY_STANDALONE_OSX || UNITY_IOS))
					_filenameExtension = NativePlugin.GetContainerFileExtensions(_codecIndex, _audioCodecIndex)[0];
#endif
				}
				filename = _filenamePrefix + "." + _filenameExtension;
				if (_appendFilenameTimestamp)
				{
					filename = GenerateTimestampedFilename(_filenamePrefix, _filenameExtension);
				}
			}
			else if (_outputType == OutputType.ImageSequence)
			{
				// [MOZ] Made the enclosing folder uniquely named, easier for extraction on iOS and simplifies scripts for processing the frames
				string fileExtension = Utils.GetImageFileExtension(NativeImageSequenceFormat);
				filename = GenerateTimestampedFilename(_filenamePrefix, null) + "/frame" + string.Format("-%0{0}d.{1}", _imageSequenceZeroDigits, fileExtension);
			}
			else if (_outputType == OutputType.NamedPipe)
			{
				_filePath = _namedPipePath;
			}

			if (_outputType == OutputType.VideoFile ||
				_outputType == OutputType.ImageSequence)
			{
				_filePath = GenerateFilePath(_outputFolderType, _outputFolderPath, filename);

				// Create target directory if doesn't exist
				String directory = Path.GetDirectoryName(_filePath);
				if (!string.IsNullOrEmpty(directory) && !Directory.Exists(directory))
				{
					Directory.CreateDirectory(directory);
				}
			}
		}

		public virtual bool PrepareCapture()
		{
			// Delete file if it already exists
			if (_outputType == OutputType.VideoFile && File.Exists(_filePath))
			{
				File.Delete(_filePath);
			}

			_numDroppedFrames = 0;
			_numDroppedEncoderFrames = 0;
			_numEncodedFrames = 0;
			_totalEncodedSeconds = 0;

#if UNITY_EDITOR_WIN || (!UNITY_EDITOR && UNITY_STANDALONE_WIN)
			if (_minimumDiskSpaceMB > 0 && _outputType == OutputType.VideoFile)
			{
				ulong freespace = 0;
				if (Utils.DriveFreeBytes(System.IO.Path.GetPathRoot(_filePath), out freespace))
				{
					_freeDiskSpaceMB = (long)(freespace / (1024 * 1024));
				}

				if (!IsEnoughDiskSpace())
				{
					Debug.LogError("[AVProMovieCapture] Not enough free space to start capture.  Stopping capture.");
					return false;
				}
			}
#endif

			if (_isRealTime)
			{
				/*if (_allowFrameRateChange)
				{
					_oldTargetFrameRate = Application.targetFrameRate;
					Application.targetFrameRate = (int)_frameRate;
				}*/
			}
			else
			{
				// Disable vsync
				if (_allowVSyncDisable && !Screen.fullScreen && QualitySettings.vSyncCount > 0)
				{
					_oldVSyncCount = QualitySettings.vSyncCount;
					QualitySettings.vSyncCount = 0;
				}

				if (_useMotionBlur && _motionBlurSamples > 1)
				{
					#if AVPRO_MOVIECAPTURE_CAPTUREDELTA_SUPPORT
					Time.captureDeltaTime = 1f / (_motionBlurSamples * _frameRate);
					#else
					Time.captureFramerate = (int)(_motionBlurSamples * _frameRate);
					#endif

					// FromTexture and FromCamera360 captures don't require a camera for rendering, so set up the motion blur component differently
					if (this is CaptureFromTexture || this is CaptureFromCamera360 || this is CaptureFromCamera360ODS)
					{
						if (_motionBlur == null)
						{
							_motionBlur = this.GetComponent<MotionBlur>();
						}
						if (_motionBlur == null)
						{
							_motionBlur = this.gameObject.AddComponent<MotionBlur>();
						}
						if (_motionBlur != null)
						{
							_motionBlur.NumSamples = _motionBlurSamples;
							_motionBlur.SetTargetSize(_targetWidth, _targetHeight);
							_motionBlur.enabled = false;
						}
					}
					// FromCamera and FromScreen use this path
					else if (_motionBlurCameras.Length > 0)
					{
						// Setup the motion blur filters where cameras are used
						foreach (Camera camera in _motionBlurCameras)
						{
							MotionBlur mb = camera.GetComponent<MotionBlur>();
							if (mb == null)
							{
								mb = camera.gameObject.AddComponent<MotionBlur>();
							}
							if (mb != null)
							{
								mb.NumSamples = _motionBlurSamples;
								mb.enabled = true;
								_motionBlur = mb;
							}
						}
					}
				}
				else
				{
					#if AVPRO_MOVIECAPTURE_CAPTUREDELTA_SUPPORT
					Time.captureDeltaTime = 1f / _frameRate;
					#else
					Time.captureFramerate = (int)_frameRate;
					#endif
				}

				// Change physics update speed
				_oldFixedDeltaTime = Time.fixedDeltaTime;
				#if AVPRO_MOVIECAPTURE_CAPTUREDELTA_SUPPORT
				Time.fixedDeltaTime = Time.captureDeltaTime;
				#else
				Time.fixedDeltaTime = 1.0f / Time.captureFramerate;
				#endif
			}

			int audioDeviceIndex = _audioDeviceIndex;
			int audioCodecIndex = _audioCodecIndex;
			bool noAudio = _noAudio;
			if (!_isRealTime)
			{
				noAudio = true;
			}

			if (_mouseCursor != null)
			{
				_mouseCursor.enabled = _captureMouseCursor;
			}

			// We if try to capture audio from Unity but there isn't an UnityAudioCapture component set
			if (!noAudio && _audioCapture == null && _audioDeviceIndex < 0)
			{
				// Try to find it locally
				_audioCapture = this.GetComponent<UnityAudioCapture>();
				if (_audioCapture == null)
				{
					// Try to find it globally
					_audioCapture = GameObject.FindObjectOfType<UnityAudioCapture>();
				}

				if (_audioCapture == null)
				{
					// Find an AudioListener to attach the UnityAudioCapture component to
					AudioListener audioListener = this.GetComponent<AudioListener>();
					if (audioListener == null)
					{
						audioListener = GameObject.FindObjectOfType<AudioListener>();
					}
					if (audioListener != null)
					{
						_audioCapture = audioListener.gameObject.AddComponent<UnityAudioCapture>();
						Debug.LogWarning("[AVProMovieCapture] Capturing audio from Unity without an UnityAudioCapture assigned so we had to create one manually (very slow).  Consider adding a UnityAudioCapture component to your scene and assigned it to this MovieCapture component.");
					}
					else
					{
						noAudio = true;
						Debug.LogWarning("[AVProMovieCapture] No audio listener found in scene.  Unable to capture audio from Untiy.");
					}
				}
				else
				{
					Debug.LogWarning("[AVProMovieCapture] Capturing audio from Unity without an UnityAudioCapture assigned so we had to search for one manually (very slow)");
				}
			}

			if (noAudio || (_audioCapture == null && _audioDeviceIndex < 0))
			{
				audioCodecIndex = audioDeviceIndex = -1;
				_audioDeviceName = "none";
				noAudio = true;
			}

			_unityAudioSampleRate = -1;
			_unityAudioChannelCount = -1;
			if (IsUsingUnityAudio())
			{
				if (!_audioCapture.enabled)
				{
					_audioCapture.enabled = true;
				}
				_unityAudioSampleRate = AudioSettings.outputSampleRate;
				_unityAudioChannelCount = _audioCapture.NumChannels;
			}

			string info = string.Format("{0}x{1} @ {2}fps [{3}]", _targetWidth, _targetHeight, _frameRate.ToString("F2"), _pixelFormat.ToString());
			if (_outputType == OutputType.VideoFile)
			{
#if UNITY_EDITOR_WIN || (!UNITY_EDITOR && UNITY_STANDALONE_WIN)
				if (_useMediaFoundationH264)
				{
					info += " vcodec:'Media Foundation H.264'";
				}
				else
#endif
				{
					info += string.Format(" vcodec:'{0}'", _codecName);
				}
				if (!noAudio)
				{
					if (_audioDeviceIndex >= 0)
					{
						info += string.Format(" audio device:'{0}'", _audioDeviceName);
					}
					else
					{
						info += string.Format(" audio device:'Unity' {0}hz {1} channels", _unityAudioSampleRate, _unityAudioChannelCount);
					}
					info += string.Format(" acodec:'{0}'", _audioCodecName);
				}

				info += string.Format(" to file: '{0}'", _filePath);
			}
			else if (_outputType == OutputType.ImageSequence)
			{
				info += string.Format(" to file: '{0}'", _filePath);
			}
			else if (_outputType == OutputType.NamedPipe)
			{
				info += string.Format(" to pipe: '{0}'", _filePath);
			}

			// If the user has overriden the vertical flip
			if (_flipVertically)
			{
				_isTopDown = !_isTopDown;
			}

			if (_outputType == OutputType.VideoFile)
			{
				// TOOD: make _frameRate floating point, or add timeLapse time system
				Debug.Log("[AVProMovieCapture] Start File Capture: " + info);
				bool useRealtimeClock = (_isRealTime && _timelapseScale <= 1);
				_handle = NativePlugin.CreateRecorderVideo(_filePath, (uint)_targetWidth, (uint)_targetHeight, _frameRate,
																	(int)_pixelFormat, _isTopDown, _codecIndex, !noAudio, _unityAudioSampleRate,
																	_unityAudioChannelCount, audioDeviceIndex, audioCodecIndex,
																	useRealtimeClock, _useMediaFoundationH264, _supportAlpha, _forceGpuFlush);
			}
			else if (_outputType == OutputType.ImageSequence)
			{
				Debug.Log("[AVProMovieCapture] Start Images Capture: " + info);
				bool useRealtimeClock = (_isRealTime && _timelapseScale <= 1);
				_handle = NativePlugin.CreateRecorderImages(_filePath, (uint)_targetWidth, (uint)_targetHeight, _frameRate,
																	(int)_pixelFormat, _isTopDown, useRealtimeClock,
																	(int)NativeImageSequenceFormat, _supportAlpha, _forceGpuFlush, _imageSequenceStartFrame);
			}
			else if (_outputType == OutputType.NamedPipe)
			{
				Debug.Log("[AVProMovieCapture] Start Pipe Capture: " + info);
				_handle = NativePlugin.CreateRecorderPipe(_filePath, (uint)_targetWidth, (uint)_targetHeight, _frameRate,
																	 (int)_pixelFormat, _isTopDown, _supportAlpha, _forceGpuFlush);
			}

			if (_handle < 0)
			{
				Debug.LogError("[AVProMovieCapture] Failed to create recorder");

				// Try to give a reason why it failed
#if UNITY_EDITOR_WIN || (!UNITY_EDITOR && UNITY_STANDALONE_WIN)
				if (!HasExtension(_filePath, ".mp4") && _useMediaFoundationH264)
				{
					Debug.LogError("[AVProMovieCapture] When using MF H.264 codec the MP4 extension must be used");
				}

				// MF H.264 encoder has a limit of Level 5.2 which is 9,437,184 luma pixels
				// but we've seen it fail slightly below this limit, so we test against 9360000
				// to offer a useful potential error message
				if (_useMediaFoundationH264 && ((_targetWidth * _targetHeight) >= 9360000))
				{
					Debug.LogError("[AVProMovieCapture] Resolution is possibly too high for the MF H.264 codec");
				}

				if (HasExtension(_filePath, ".mp4") && !_useMediaFoundationH264 || _codecIndex == 0)
				{
					Debug.LogError("[AVProMovieCapture] Uncompressed video codec not supported with MP4 extension, use AVI instead for uncompressed");
				}
#endif

				StopCapture();
			}

// (mac|i)OS only for now
#if UNITY_EDITOR_OSX || (!UNITY_EDITOR && (UNITY_STANDALONE_OSX || UNITY_IOS))
			SetupErrorHandler();
#endif
			return (_handle >= 0);
		}

#if UNITY_EDITOR_OSX || (!UNITY_EDITOR && (UNITY_STANDALONE_OSX || UNITY_IOS))

		static Dictionary<int, CaptureBase> _HandleToCaptureMap = new Dictionary<int, CaptureBase>();

		private void SetupErrorHandler()
		{
			NativePlugin.ErrorHandlerDelegate errorHandlerDelegate = new NativePlugin.ErrorHandlerDelegate(ErrorHandler);
			System.IntPtr func = Marshal.GetFunctionPointerForDelegate(errorHandlerDelegate);
			NativePlugin.SetErrorHandler(_handle, func);
			_HandleToCaptureMap.Add(_handle, this);
		}

		private void CleanupErrorHandler()
		{
			_HandleToCaptureMap.Remove(_handle);
		}

#if ENABLE_IL2CPP
		[MonoPInvokeCallback(typeof(NativePlugin.ErrorHandlerDelegate))]
#endif
		private static void ErrorHandler(int handle, int domain, int code, string message)
		{
			CaptureBase capture;
			if (_HandleToCaptureMap.TryGetValue(handle, out capture))
			{
				capture.ActualErrorHandler(domain, code, message);
			}
		}

		private void ActualErrorHandler(int domain, int code, string message) {
			if (_capturing)
			{
				CancelCapture();
				Debug.LogError("Capture cancelled");
			}
			Debug.LogErrorFormat("Error: domain: {0}, code: {1}, message: {2}", domain, code, message);
		}
#endif

		public void QueueStartCapture()
		{
			_queuedStartCapture = true;
		}

		public bool StartCapture()
		{
			if (_capturing)
			{
				return false;
			}

			if (_waitForEndOfFrame == null)
			{
				// Start() hasn't happened yet, so queue the StartCapture
				QueueStartCapture();
				return false;
			}

			if (_handle < 0)
			{
				if (!PrepareCapture())
				{
					return false;
				}
			}

			if (_handle >= 0)
			{
				if (IsUsingUnityAudio())
				{
					_audioCapture.FlushBuffer();
				}

				if (!NativePlugin.Start(_handle))
				{
					StopCapture(true);
					Debug.LogError("[AVProMovieCapture] Failed to start recorder");
					return false;
				}
				ResetFPS();
				_captureStartTime = Time.realtimeSinceStartup;

				// NOTE: We set this to the elapsed time so that the first frame is captured immediately
				_timeSinceLastFrame = GetSecondsPerCaptureFrame();

				#if AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
				if (!_isRealTime && _timelineController != null)
				{
					_timelineController.StartCapture();
				}
				#endif

				_capturing = true;
				_paused = false;

				if (_startDelay != StartDelayMode.None)
				{
					_startDelayTimer = 0f;
					_startPaused = true;
					PauseCapture();
				}
			}

			return _capturing;
		}

		public void PauseCapture()
		{
			if (_capturing && !_paused)
			{
				if (IsUsingUnityAudio())
				{
					_audioCapture.enabled = false;
				}
				NativePlugin.Pause(_handle);

				if (!_isRealTime)
				{
					// TODO: should be store the timeScale value and restore it instead of assuming timeScale == 1.0?
					Time.timeScale = 0f;
				}

				_paused = true;
				ResetFPS();
			}
		}

		public void ResumeCapture()
		{
			if (_capturing && _paused)
			{
				if (IsUsingUnityAudio())
				{
					_audioCapture.FlushBuffer();
					_audioCapture.enabled = true;
				}

				NativePlugin.Start(_handle);

				if (!_isRealTime)
				{
					Time.timeScale = 1f;
				}

				_paused = false;
				if (_startPaused)
				{
					_captureStartTime = Time.realtimeSinceStartup;
					_startPaused = false;
				}
			}
		}

		public void CancelCapture()
		{
			StopCapture(true);

			// Delete file
			if (_outputType == OutputType.VideoFile && File.Exists(_filePath))
			{
				File.Delete(_filePath);
			}
		}

		public virtual void UnprepareCapture()
		{
			if (_mouseCursor != null)
			{
				_mouseCursor.enabled = false;
			}
#if UNITY_EDITOR_OSX || (!UNITY_EDITOR && (UNITY_STANDALONE_OSX || UNITY_IOS))
			CleanupErrorHandler();
#endif
		}

		public static string LastFileSaved
		{
			get
			{
#if UNITY_EDITOR
				return UnityEditor.EditorPrefs.GetString("AVProMovieCapture-LastSavedFile", string.Empty);
#else
				return PlayerPrefs.GetString("AVProMovieCapture-LastSavedFile", string.Empty);
#endif
			}
			set
			{
				PlayerPrefs.SetString("AVProMovieCapture-LastSavedFile", value);
#if UNITY_EDITOR
				UnityEditor.EditorPrefs.SetString("AVProMovieCapture-LastSavedFile", value);
#endif
			}
		}

		protected void RenderThreadEvent(NativePlugin.PluginEvent renderEvent)
		{
#if AVPRO_MOVIECAPTURE_GLISSUEEVENT_52
			if (_renderEventFunction == System.IntPtr.Zero)
			{
				SetupRenderFunctions();
			}
#endif
			if (renderEvent == NativePlugin.PluginEvent.CaptureFrameBuffer)
			{
#if AVPRO_MOVIECAPTURE_GLISSUEEVENT_52
				GL.IssuePluginEvent(_renderEventFunction, NativePlugin.PluginID | (int)renderEvent | _handle);
#else
				GL.IssuePluginEvent(NativePlugin.PluginID | (int)renderEvent | _handle);
#endif
			}
			else if (renderEvent == NativePlugin.PluginEvent.FreeResources)
			{
				int eventId = NativePlugin.PluginID | (int)renderEvent;
#if AVPRO_MOVIECAPTURE_GLISSUEEVENT_52
				GL.IssuePluginEvent(_freeEventFunction, eventId);
#else
				GL.IssuePluginEvent(eventId);
#endif
			}
		}

		public virtual void StopCapture(bool skipPendingFrames = false, bool ignorePendingFileWrites = false)
		{
			UnprepareCapture();

			if (_capturing)
			{
				Debug.Log("[AVProMovieCapture] Stopping capture " + _handle);
				_capturing = false;
			}

			bool applyPostOperations = false;
			if (_handle >= 0)
			{
				NativePlugin.Stop(_handle, skipPendingFrames);

				// Free the recorder, or if the file is still being written, store the action to be invoked where it is complete
				if (ignorePendingFileWrites || NativePlugin.IsFileWritingComplete(_handle))
				{
					NativePlugin.FreeRecorder(_handle);
				}
				else
				{
					if (_fileWritingAction == null)
					{
						_pendingFileWrites.Add(new FileWritingHandler(this._filePath, _handle));
					}
				}
				if (_fileWritingAction != null)
				{
					_fileWritingAction.Invoke(new FileWritingHandler(this._filePath, _handle));
				}
				_handle = -1;

				// Save the last captured path
				if (!skipPendingFrames && !string.IsNullOrEmpty(_filePath))
				{
					if (_outputType == OutputType.VideoFile)
					{
						LastFileSaved = _filePath;
						applyPostOperations = true;
					}
					else if (_outputType == OutputType.ImageSequence)
					{
						LastFileSaved = System.IO.Path.GetDirectoryName(_filePath);
					}
				}

				#if AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
				if (_timelineController != null)
				{
					_timelineController.StopCapture();
				}
				#endif
			}

			RenderThreadEvent(NativePlugin.PluginEvent.FreeResources);

			_fileInfo = null;

			if (_audioCapture)
			{
				_audioCapture.enabled = false;
			}

			if (_motionBlur)
			{
				_motionBlur.enabled = false;
			}

			// Restore Unity timing
			Time.captureFramerate = 0;
			//Application.targetFrameRate = _oldTargetFrameRate;
			//_oldTargetFrameRate = -1;

			if (_oldFixedDeltaTime > 0f)
			{
				Time.fixedDeltaTime = _oldFixedDeltaTime;
			}
			_oldFixedDeltaTime = 0f;

			if (_oldVSyncCount > 0)
			{
				QualitySettings.vSyncCount = _oldVSyncCount;
				_oldVSyncCount = 0;
			}

			_motionBlur = null;

			if (_texture != null)
			{
				Destroy(_texture);
				_texture = null;
			}

			if (applyPostOperations)
			{
				ApplyPostOperations(_filePath);
			}
		}

		protected void ApplyPostOperations(string path)
		{
#if UNITY_EDITOR_WIN || (!UNITY_EDITOR && UNITY_STANDALONE_WIN)
			if (_postCaptureSettings.windows.writeFastStartStreamingForMp4 && HasExtension(path, ".mp4"))
			{
				try
				{
					if (!MP4FileProcessing.ApplyFastStart(path, false))
					/*MP4FileProcessing.Options options = new MP4FileProcessing.Options();
					options.applyFastStart = true;
					options.applyStereoMode = false;
					options.stereoMode = MP4FileProcessing.StereoMode.StereoLeftRight;
					if (MP4FileProcessing.Process(path, false, options))*/
					{
						Debug.LogWarning("[AVProMovieCapture] failed moving atom 'moov' to start of file for fast streaming");
					}
				}
				catch (System.Exception e)
				{
					Debug.LogException(e);
				}
			}
#endif
		}

		private void ToggleCapture()
		{
			if (_capturing)
			{
				//_queuedStopCapture = true;
				//_queuedStartCapture = false;
				StopCapture();
			}
			else
			{
				//_queuedStartCapture = true;
				//_queuedStopCapture = false;
				StartCapture();
			}
		}

		private bool IsEnoughDiskSpace()
		{
			bool result = true;
#if UNITY_EDITOR_WIN || (!UNITY_EDITOR && UNITY_STANDALONE_WIN)
			long fileSizeMB = GetCaptureFileSize() / (1024 * 1024);

			if ((_freeDiskSpaceMB - fileSizeMB) < _minimumDiskSpaceMB)
			{
				result = false;
			}
#endif
			return result;
		}

		private void LateUpdate()
		{
			if (_handle >= 0 && !_paused)
			{
				CheckFreeDiskSpace();
			}

			// Resume capture if a start delay has been specified
			if (IsCapturing() && IsPaused() && _numEncodedFrames == 0)
			{
				float delta = 0f;
				if (_startDelay == StartDelayMode.GameSeconds)
				{
					delta = Time.deltaTime;
				}
				else if (_startDelay == StartDelayMode.RealSeconds)
				{
					delta = Time.unscaledDeltaTime;
				}
				if (delta > 0f)
				{
					_startDelayTimer += delta;
					if (IsStartDelayComplete())
					{
						ResumeCapture();
					}
				}
			}

			RemoveCompletedFileWrites();

			#if AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
			if (IsCapturing() && !IsPaused() && !_isRealTime && _timelineController != null)
			{
				_timelineController.UpdateFrame();
			}
			#endif

			UpdateFrame();
		}

		private void RemoveCompletedFileWrites()
		{
			for (int i = _pendingFileWrites.Count - 1; i >= 0; i--)
			{
				FileWritingHandler handler = _pendingFileWrites[i];
				if (handler.IsFileReady())
				{
					_pendingFileWrites.RemoveAt(i);
				}
			}
		}

		private void CheckFreeDiskSpace()
		{
			if (_minimumDiskSpaceMB > 0)
			{
				if (!IsEnoughDiskSpace())
				{
					Debug.LogWarning("[AVProMovieCapture] Free disk space getting too low.  Stopping capture.");
					StopCapture(true);
				}
			}
		}

		protected bool IsStartDelayComplete()
		{
			bool result = false;
			if (_startDelay == StartDelayMode.None)
			{
				result = true;
			}
			else if (_startDelay == StartDelayMode.GameSeconds ||
					_startDelay == StartDelayMode.RealSeconds)
			{
				result = (_startDelayTimer >= _startDelaySeconds);
			}
			return result;
		}

		protected bool IsProgressComplete()
		{
			bool result = false;
			if (_stopMode != StopMode.None)
			{
				switch (_stopMode)
				{
					case StopMode.FramesEncoded:
						result = (_numEncodedFrames >= _stopFrames);
						break;
					case StopMode.SecondsEncoded:
						result = (_totalEncodedSeconds >= _stopSeconds);
						break;
					case StopMode.SecondsElapsed:
						if (!_startPaused && !_paused)
						{
							result = ((Time.realtimeSinceStartup - _captureStartTime) >= _stopSeconds);
						}
						break;
				}
			}
			return result;
		}

		public float GetProgress()
		{
			float result = 0f;
			if (_stopMode != StopMode.None)
			{
				switch (_stopMode)
				{
					case StopMode.FramesEncoded:
						result = (_numEncodedFrames / (float)_stopFrames);
						break;
					case StopMode.SecondsEncoded:
						result = ((_numEncodedFrames / _frameRate) / _stopSeconds);
						break;
					case StopMode.SecondsElapsed:
						if (!_startPaused && !_paused)
						{
							result = ((Time.realtimeSinceStartup - _captureStartTime) / _stopSeconds);
						}
						break;
				}
			}
			return result;
		}

		protected float GetSecondsPerCaptureFrame()
		{
			float timelapseScale = (float)_timelapseScale;
			if (!_isRealTime)
			{
				timelapseScale = 1f;
			}
			float captureFrameRate = _frameRate / timelapseScale;
			float secondsPerFrame = 1f / captureFrameRate;
			return secondsPerFrame;
		}

		protected bool CanOutputFrame()
		{
			bool result = false;
			if (_handle >= 0)
			{
				if (_isRealTime)
				{
					if (NativePlugin.IsNewFrameDue(_handle))
					{
						result = (_timeSinceLastFrame >= GetSecondsPerCaptureFrame());
						//result = true;
					}
				}
				else
				{
					const int WatchDogLimit = 100;
					int watchdog = 0;
					if (_outputType != OutputType.NamedPipe)
					{
						// Wait for the encoder to have an available buffer
						// The watchdog prevents an infinite while loop
						while (_handle >= 0 && !NativePlugin.IsNewFrameDue(_handle) && watchdog < WatchDogLimit)
						{
							System.Threading.Thread.Sleep(1);
							watchdog++;
						}
					}

					// Return handle status as it may have closed elsewhere
					result = (_handle >= 0) && (watchdog < WatchDogLimit);
				}
			}
			return result;
		}

		protected void TickFrameTimer()
		{
			_timeSinceLastFrame += Time.unscaledDeltaTime;
		}

		protected void RenormTimer()
		{
			float secondsPerFrame = GetSecondsPerCaptureFrame();
			if (_timeSinceLastFrame >= secondsPerFrame)
			{
				_timeSinceLastFrame -= secondsPerFrame;
			}
		}

		public virtual Texture GetPreviewTexture()
		{
			return null;
		}

		public virtual void UpdateFrame()
		{
			if (Input.GetKeyDown(_captureKey))
			{
				ToggleCapture();
			}

			if (_handle >= 0 && !_paused)
			{
				_numDroppedFrames = NativePlugin.GetNumDroppedFrames(_handle);
				_numDroppedEncoderFrames = NativePlugin.GetNumDroppedEncoderFrames(_handle);
				_numEncodedFrames = NativePlugin.GetNumEncodedFrames(_handle);
				_totalEncodedSeconds = NativePlugin.GetEncodedSeconds(_handle);

				if (IsProgressComplete())
				{
					_queuedStopCapture = true;
				}
			}

			if (_queuedStopCapture)
			{
				_queuedStopCapture = false;
				_queuedStartCapture = false;
				StopCapture();
			}
			if (_queuedStartCapture)
			{
				_queuedStartCapture = false;
				StartCapture();
			}
		}

		private float _fps;
		private int _frameTotal;

		public float FPS { get { return _fps; } }
		public float FramesTotal { get { return _frameTotal; } }

		private int _frameCount;
		private float _startFrameTime;

		protected void ResetFPS()
		{
			_frameCount = 0;
			_frameTotal = 0;
			_fps = 0.0f;
			_startFrameTime = 0.0f;
		}

		public void UpdateFPS()
		{
			_frameCount++;
			_frameTotal++;

			float timeNow = Time.realtimeSinceStartup;
			float timeDelta = timeNow - _startFrameTime;
			if (timeDelta >= 1.0f)
			{
				_fps = (float)_frameCount / timeDelta;
				_frameCount = 0;
				_startFrameTime = timeNow;
			}
		}

		protected int GetCameraAntiAliasingLevel(Camera camera)
		{
			int aaLevel = QualitySettings.antiAliasing;
			if (aaLevel == 0)
			{
				aaLevel = 1;
			}

			if (_renderAntiAliasing > 0)
			{
				aaLevel = _renderAntiAliasing;
			}

			if (aaLevel != 1 && aaLevel != 2 && aaLevel != 4 && aaLevel != 8)
			{
				Debug.LogError("[AVProMovieCapture] Invalid antialiasing value, must be 1, 2, 4 or 8.  Defaulting to 1. >> " + aaLevel);
				aaLevel = 1;
			}

			if (aaLevel != 1)
			{
				if (camera.actualRenderingPath == RenderingPath.DeferredLighting
#if AVPRO_MOVIECAPTURE_DEFERREDSHADING
					|| camera.actualRenderingPath == RenderingPath.DeferredShading
#endif
					)
				{
					Debug.LogWarning("[AVProMovieCapture] Not using antialiasing because MSAA is not supported by camera render path " + camera.actualRenderingPath);
					aaLevel = 1;
				}
			}
			return aaLevel;
		}

		private void ConfigureCodec()
		{
			NativePlugin.Init();
			SelectCodec(false);
			if (_codecIndex >= 0)
			{
				NativePlugin.ConfigureVideoCodec(_codecIndex);
			}
			//AVProMovieCapture.Deinit();
		}

		public long GetCaptureFileSize()
		{
			long result = 0;
#if UNITY_EDITOR_OSX || (!UNITY_EDITOR && (UNITY_STANDALONE_OSX || UNITY_IOS))
			result = NativePlugin.GetFileSize(_handle);
#elif !UNITY_WEBPLAYER
			if (_handle >= 0 && _outputType == OutputType.VideoFile)
			{
				if (_fileInfo == null && File.Exists(_filePath))
				{
					_fileInfo = new System.IO.FileInfo(_filePath);
				}
				if (_fileInfo != null)
				{
					_fileInfo.Refresh();
					result = _fileInfo.Length;
				}
			}
#endif
			return result;
		}

		public static void GetResolution(Resolution res, ref int width, ref int height)
		{
			switch (res)
			{
				case Resolution.POW2_8192x8192:
					width = 8192; height = 8192;
					break;
				case Resolution.POW2_8192x4096:
					width = 8192; height = 4096;
					break;
				case Resolution.POW2_4096x4096:
					width = 4096; height = 4096;
					break;
				case Resolution.POW2_4096x2048:
					width = 4096; height = 2048;
					break;
				case Resolution.POW2_2048x4096:
					width = 2048; height = 4096;
					break;
				case Resolution.UHD_3840x2160:
					width = 3840; height = 2160;
					break;
				case Resolution.UHD_3840x2048:
					width = 3840; height = 2048;
					break;
				case Resolution.UHD_3840x1920:
					width = 3840; height = 1920;
					break;
				case Resolution.POW2_2048x2048:
					width = 2048; height = 2048;
					break;
				case Resolution.POW2_2048x1024:
					width = 2048; height = 1024;
					break;
				case Resolution.HD_1920x1080:
					width = 1920; height = 1080;
					break;
				case Resolution.HD_1280x720:
					width = 1280; height = 720;
					break;
				case Resolution.SD_1024x768:
					width = 1024; height = 768;
					break;
				case Resolution.SD_800x600:
					width = 800; height = 600;
					break;
				case Resolution.SD_800x450:
					width = 800; height = 450;
					break;
				case Resolution.SD_640x480:
					width = 640; height = 480;
					break;
				case Resolution.SD_640x360:
					width = 640; height = 360;
					break;
				case Resolution.SD_320x240:
					width = 320; height = 240;
					break;
			}
		}

		// Returns the next multiple of 4 or the same value if it's already a multiple of 4
		protected static int NextMultipleOf4(int value)
		{
			return (value + 3) & ~0x03;
		}
	}
}