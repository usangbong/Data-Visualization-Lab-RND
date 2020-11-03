#if UNITY_2017_1_OR_NEWER
	#define AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
#endif
#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System.Collections;

//-----------------------------------------------------------------------------
// Copyright 2012-2019 RenderHeads Ltd.  All rights reserved.
//-----------------------------------------------------------------------------

namespace RenderHeads.Media.AVProMovieCapture.Editor
{
	[CanEditMultipleObjects]
	[CustomEditor(typeof(CaptureBase), true)]
	public class CaptureBaseEditor : UnityEditor.Editor
	{
		private const string SettingsPrefix = "AVProMovieCapture-BaseEditor-";

		public readonly static string[] ResolutionStrings = { "8192x8192 (1:1)", "8192x4096 (2:1)", "4096x4096 (1:1)", "4096x2048 (2:1)", "2048x4096 (1:2)", "3840x2160 (16:9)", "3840x2048 (15:8)", "3840x1920 (2:1)", "2048x2048 (1:1)", "2048x1024 (2:1)", "1920x1080 (16:9)", "1280x720 (16:9)", "1024x768 (4:3)", "800x600 (4:3)", "800x450 (16:9)", "640x480 (4:3)", "640x360 (16:9)", "320x240 (4:3)", "Original", "Custom" };

		private static bool _isTrialVersion = false;
		private SerializedProperty _propCaptureKey;
		private SerializedProperty _propListCodecsOnStart;
		private SerializedProperty _propMinimumDiskSpaceMB;
		private SerializedProperty _propPersistAcrossSceneLoads;

		private SerializedProperty _propIsRealtime;

		private SerializedProperty _propOutputType;
		private SerializedProperty _propImageSequenceFormatWindows;
		private SerializedProperty _propImageSequenceFormatMacOS;
		private SerializedProperty _propImageSequenceFormatIOS;
		private SerializedProperty _propImageSequenceStartFrame;
		private SerializedProperty _propImageSequenceZeroDigits;
		private SerializedProperty _propOutputFolderType;
		private SerializedProperty _propOutputFolderPath;
		private SerializedProperty _propAppendFilenameTimestamp;
		private SerializedProperty _propFileNamePrefix;
		private SerializedProperty _propAllowManualFileExtension;
		private SerializedProperty _propFileNameExtension;
		private SerializedProperty _propForceFileName;
		private SerializedProperty _propNamedPipePath;

		private SerializedProperty _propVideoCodecPriorityWindows;
		private SerializedProperty _propVideoCodecPriorityMacOS;
		private SerializedProperty _propUseMediaFoundationH264;
		private SerializedProperty _propForceVideoCodecIndexWindows;
		private SerializedProperty _propForceVideoCodecIndexMacOS;
		private SerializedProperty _propForceVideoCodecIndexIOS;

		private SerializedProperty _propAudioCodecPriority;
		private SerializedProperty _propForceAudioCodecIndex;
		private SerializedProperty _propForceAudioDeviceIndex;
		private SerializedProperty _propNoAudio;
		private SerializedProperty _propUnityAudioCapture;

		private SerializedProperty _propStartTrigger;
		private SerializedProperty _propStartDelay;
		private SerializedProperty _propStartDelaySeconds;

		private SerializedProperty _propStopMode;
		private SerializedProperty _propStopFrames;
		private SerializedProperty _propStopSeconds;

		private SerializedProperty _propPostFastStartMp4;

		private SerializedProperty _propDownScale;
		private SerializedProperty _propMaxVideoSize;
		private SerializedProperty _propFrameRate;
		private SerializedProperty _propTimelapseScale;
		private SerializedProperty _propFlipVertically;
		private SerializedProperty _propSupportAlpha;
		private SerializedProperty _propForceGpuFlush;
		private SerializedProperty _propWaitForEndOfFrame;

		private SerializedProperty _propUseMotionBlur;
		private SerializedProperty _propMotionBlurSamples;
		private SerializedProperty _propMotionBlurCameras;

		private SerializedProperty _propAllowVsyncDisable;
		private SerializedProperty _propSupportTextureRecreate;
		#if AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
		private SerializedProperty _propTimelineController;
		#endif

		private static bool _isExpandedStartStop = false;
		private static bool _isExpandedOutput = false;
		private static bool _isExpandedVisual = false;
		private static bool _isExpandedAudio = false;
		private static bool _isExpandedPost = false;
		private static bool _isExpandedMisc = false;
		private static bool _isExpandedTrial = true;
		private static bool _isExpandedAbout = false;
		private static NativePlugin.Platform _selectedPlatform = NativePlugin.Platform.Windows;
		private static GUIStyle _stylePlatformBox = null;

		protected CaptureBase _baseCapture;

		public override void OnInspectorGUI()
		{
			// Warning if the base component is used
			if (this.target.GetType() == typeof(CaptureBase))
			{
				GUI.color = Color.yellow;
				GUILayout.BeginVertical("box");
				GUILayout.TextArea("Error: This is not a component, this is the base class.\n\nPlease add one of the components\n(eg:CaptureFromScene / CaptureFromCamera etc)");
				GUILayout.EndVertical();
				return;
			}

			if (_stylePlatformBox == null)
			{
				_stylePlatformBox = new GUIStyle(GUI.skin.box);
				_stylePlatformBox.padding.top = 0;
				_stylePlatformBox.padding.bottom = 0;
			}

			GUI_Header();
			GUI_BaseOptions();
		}

		protected virtual void GUI_User()
		{

		}

		protected void GUI_Header()
		{
			// Describe the watermark for trial version
			if (_isTrialVersion)
			{
				EditorUtils.DrawSectionColored("- AVPRO MOVIE CAPTURE -\nTRIAL VERSION", ref _isExpandedTrial, DrawTrialMessage, Color.magenta, Color.magenta, Color.magenta);
			}

			// Button to launch the capture window
			{
				GUI.backgroundColor = new Color(0.96f, 0.25f, 0.47f);
				if (GUILayout.Button("\n◄ Open Movie Capture Window ►\n"))
				{
					CaptureEditorWindow.Init();
				}
				GUI.backgroundColor = Color.white;
			}
		}

		protected void DrawTrialMessage()
		{
			string message = "The free trial version is watermarked.  Upgrade to the full package to remove the watermark.";

			GUI.backgroundColor = Color.yellow;
			EditorGUILayout.BeginVertical(GUI.skin.box);
			//GUI.color = Color.yellow;
			//GUILayout.Label("AVPRO MOVIE CAPTURE - FREE TRIAL VERSION", EditorStyles.boldLabel);
			GUI.color = Color.white;
			GUILayout.Label(message, EditorStyles.wordWrappedLabel);
			if (GUILayout.Button("Upgrade Now"))
			{
				Application.OpenURL("https://www.assetstore.unity3d.com/en/#!/content/2670");
			}
			EditorGUILayout.EndVertical();
			GUI.backgroundColor = Color.white;
			GUI.color = Color.white;
		}

		protected void GUI_BaseOptions()
		{
			serializedObject.Update();

			if (_baseCapture == null)
			{
				return;
			}

			//DrawDefaultInspector();

			if (!_baseCapture.IsCapturing())
			{
				GUILayout.Space(8f);
				EditorUtils.BoolAsDropdown("Capture Mode", _propIsRealtime, "Realtime Capture", "Offline Render");
				GUILayout.Space(8f);

				if (serializedObject.ApplyModifiedProperties())
				{
					EditorUtility.SetDirty(target);
				}

				GUI_User();

				// After the user mode we must update the serialised object again
				serializedObject.Update();

				EditorUtils.DrawSection("Start / Stop", ref _isExpandedStartStop, GUI_StartStop);
				EditorUtils.DrawSection("Output", ref _isExpandedOutput, GUI_OutputFilePath);
				EditorUtils.DrawSection("Visual", ref _isExpandedVisual, GUI_Visual);
				EditorUtils.DrawSection("Audio", ref _isExpandedAudio, GUI_Audio);
				EditorUtils.DrawSection("Post", ref _isExpandedPost, GUI_Post);
				EditorUtils.DrawSection("Misc", ref _isExpandedMisc, GUI_Misc);
				EditorUtils.DrawSection("About", ref _isExpandedAbout, GUI_About);

				if (serializedObject.ApplyModifiedProperties())
				{
					EditorUtility.SetDirty(target);
				}

				GUI_Controls();
			}
			else
			{
				GUI_Stats();
				GUI_Progress();
				GUI_Controls();
			}
		}

		protected void GUI_Progress()
		{
			if (_baseCapture == null)
			{
				return;
			}

			if (_propStopMode.enumValueIndex != (int)StopMode.None)
			{
				Rect r = GUILayoutUtility.GetRect(128f, EditorStyles.label.CalcHeight(GUIContent.none, 32f), GUILayout.ExpandWidth(true));
				float progress = _baseCapture.GetProgress();
				EditorGUI.ProgressBar(r, progress, (progress * 100f).ToString("F1") + "%");
			}
		}

		protected void GUI_Stats()
		{
			if (_baseCapture == null)
			{
				return;
			}

			if (Application.isPlaying && _baseCapture.IsCapturing())
			{
				CaptureEditorWindow.DrawBaseCapturingGUI(_baseCapture);
				if (!_baseCapture._isRealTime)
				{
					long lastFileSize = _baseCapture.GetCaptureFileSize();
					uint lastEncodedSeconds = (uint)Mathf.FloorToInt((float)_baseCapture.NumEncodedFrames / _baseCapture.FrameRate);
					if (_baseCapture._isRealTime)
					{
						lastEncodedSeconds = _baseCapture.TotalEncodedSeconds;
					}
					uint lastEncodedMinutes = lastEncodedSeconds / 60;
					lastEncodedSeconds = lastEncodedSeconds % 60;
					uint lastEncodedFrame = _baseCapture.NumEncodedFrames % (uint)_baseCapture.FrameRate;

					EditorGUILayout.BeginVertical("box");
					EditorGUI.indentLevel++;

					EditorGUILayout.LabelField("File Size", ((float)lastFileSize / (1024f * 1024f)).ToString("F1") + "MB");
					EditorGUILayout.LabelField("Video Length", lastEncodedMinutes.ToString("00") + ":" + lastEncodedSeconds.ToString("00") + "." + lastEncodedFrame.ToString("000"));

					EditorGUI.indentLevel--;
					EditorGUILayout.EndVertical();
				}
			}
		}

		protected void GUI_Controls()
		{
			if (_baseCapture == null)
			{
				return;
			}

			GUILayout.Space(8.0f);

			EditorGUI.BeginDisabledGroup(!Application.isPlaying);
			{
				if (!_baseCapture.IsCapturing())
				{
					GUI.backgroundColor = Color.green;
					string startString = "Start Capture";
					if (!_baseCapture._isRealTime)
					{
						startString = "Start Render";
					}
					if (GUILayout.Button(startString, GUILayout.Height(32f)))
					{
						_baseCapture.SelectCodec(false);
						_baseCapture.SelectAudioDevice(false);
						// We have to queue the start capture otherwise Screen.width and height aren't correct
						_baseCapture.QueueStartCapture();
					}
					GUI.backgroundColor = Color.white;
				}
				else
				{
					GUILayout.BeginHorizontal();
					if (!_baseCapture.IsPaused())
					{
						GUI.backgroundColor = Color.yellow;
						if (GUILayout.Button("Pause", GUILayout.Height(32f)))
						{
							_baseCapture.PauseCapture();
						}
					}
					else
					{
						GUI.backgroundColor = Color.green;
						if (GUILayout.Button("Resume", GUILayout.Height(32f)))
						{
							_baseCapture.ResumeCapture();
						}
					}
					GUI.backgroundColor = Color.cyan;
					if (GUILayout.Button("Cancel", GUILayout.Height(32f)))
					{
						_baseCapture.CancelCapture();
					}
					GUI.backgroundColor = Color.red;
					if (GUILayout.Button("Stop", GUILayout.Height(32f)))
					{
						_baseCapture.StopCapture();
					}
					GUI.backgroundColor = Color.white;
					GUILayout.EndHorizontal();
				}
			}
			EditorGUI.EndDisabledGroup();

			EditorGUILayout.Space();
			EditorGUI.BeginDisabledGroup(string.IsNullOrEmpty(CaptureBase.LastFileSaved));
			GUILayout.BeginHorizontal();
			if (GUILayout.Button("Browse Last"))
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
			EditorGUI.EndDisabledGroup();
		}

		protected void GUI_OutputFilePath()
		{
			EditorUtils.EnumAsDropdown("Output Type", _propOutputType, EditorUtils.OutputTypeNames);
			if (_propOutputType.enumValueIndex == (int)CaptureBase.OutputType.VideoFile ||
				_propOutputType.enumValueIndex == (int)CaptureBase.OutputType.ImageSequence)
			{
				bool isImageSequence = (_propOutputType.enumValueIndex == (int)CaptureBase.OutputType.ImageSequence);

				if (isImageSequence)
				{
					BeginPlatformSelection();
					if (_selectedPlatform == NativePlugin.Platform.Windows)
					{
						EditorUtils.EnumAsDropdown("Format", _propImageSequenceFormatWindows, Utils.WindowsImageSequenceFormatNames);
					}
					else if (_selectedPlatform == NativePlugin.Platform.macOS)
					{
						EditorUtils.EnumAsDropdown("Format", _propImageSequenceFormatMacOS, Utils.MacOSImageSequenceFormatNames);
					}
					else if (_selectedPlatform == NativePlugin.Platform.iOS)
					{
						EditorUtils.EnumAsDropdown("Format", _propImageSequenceFormatIOS, Utils.IOSImageSequenceFormatNames);
					}
					EndPlatformSelection();
					GUILayout.Space(8f);
				}

				GUILayout.Label("Folder", EditorStyles.boldLabel);
				EditorGUILayout.PropertyField(_propOutputFolderType, new GUIContent("Folder"));
				if (_propOutputFolderType.enumValueIndex == (int)CaptureBase.OutputPath.Absolute)
				{
					EditorGUILayout.BeginHorizontal();
					EditorGUILayout.PropertyField(_propOutputFolderPath, new GUIContent("Path"));
					if (GUILayout.Button(">", GUILayout.Width(22)))
					{
						_propOutputFolderPath.stringValue = EditorUtility.SaveFolderPanel("Select Folder To Store Video Captures", System.IO.Path.GetFullPath(System.IO.Path.Combine(Application.dataPath, "../")), "");
					}
					EditorGUILayout.EndHorizontal();
				}
				else
				{
					EditorGUILayout.PropertyField(_propOutputFolderPath, new GUIContent("Subfolder(s)"));
				}

				GUILayout.Label("File Name", EditorStyles.boldLabel);

				if (!isImageSequence)
				{
					EditorGUILayout.PropertyField(_propFileNamePrefix, new GUIContent("Prefix"));
					EditorGUILayout.PropertyField(_propAppendFilenameTimestamp, new GUIContent("Append Timestamp"));
					EditorGUILayout.PropertyField(_propAllowManualFileExtension, new GUIContent("Manual Extension"));
					if (_propAllowManualFileExtension.boolValue)
					{
						EditorGUILayout.PropertyField(_propFileNameExtension, new GUIContent("Extension"));
					}
				}

				if (isImageSequence)
				{
					EditorGUILayout.PropertyField(_propFileNamePrefix, new GUIContent("Prefix"));
					EditorGUILayout.PropertyField(_propImageSequenceStartFrame, new GUIContent("Start Frame"));
					EditorGUILayout.PropertyField(_propImageSequenceZeroDigits, new GUIContent("Zero Digits"));
				}
			}
			else
			{
				EditorGUILayout.PropertyField(_propNamedPipePath, new GUIContent("Pipe Path"));
			}


			/*// File path
			EditorGUILayout.LabelField("File Path", EditorStyles.boldLabel);
			EditorGUI.indentLevel++;
			_outputFolderIndex = EditorGUILayout.Popup("Relative to", _outputFolderIndex, _outputFolders);
			if (_outputFolderIndex == 0 || _outputFolderIndex == 1)
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
			EditorGUI.indentLevel--;*/
		}

		protected void GUI_StartStop()
		{
			EditorGUILayout.PropertyField(_propCaptureKey, new GUIContent("Toggle Key"));

			EditorGUILayout.Separator();

			EditorGUILayout.PropertyField(_propStartTrigger, new GUIContent("Start Mode"));
			EditorGUILayout.PropertyField(_propStartDelay, new GUIContent("Start Delay"));

			if ((StartDelayMode)_propStartDelay.enumValueIndex == StartDelayMode.RealSeconds ||
				(StartDelayMode)_propStartDelay.enumValueIndex == StartDelayMode.GameSeconds)
			{
				EditorGUILayout.PropertyField(_propStartDelaySeconds, new GUIContent("Seconds"));
			}

			EditorGUILayout.Separator();

			EditorGUILayout.PropertyField(_propStopMode, new GUIContent("Stop Mode"));
			if ((StopMode)_propStopMode.enumValueIndex == StopMode.FramesEncoded)
			{
				EditorGUILayout.PropertyField(_propStopFrames, new GUIContent("Frames"));
			}
			else if ((StopMode)_propStopMode.enumValueIndex == StopMode.SecondsElapsed || (StopMode)_propStopMode.enumValueIndex == StopMode.SecondsEncoded)
			{
				EditorGUILayout.PropertyField(_propStopSeconds, new GUIContent("Seconds"));
			}
		}

		private void BeginPlatformSelection()
		{
			GUILayout.BeginVertical(_stylePlatformBox);
			int rowCount = 0;
			int platformIndex = (int)_selectedPlatform;
			for (int i = 0; i < NativePlugin.PlatformNames.Length; i++)
			{
				if (i % 3 == 0)
				{
					GUILayout.BeginHorizontal();
					rowCount++;
				}
				
				Color hilight = Color.yellow;
				
				if (i == platformIndex)
				{
				}
				else
				{
					// Unselected, unmodified
					if (EditorGUIUtility.isProSkin)
					{
						GUI.backgroundColor = Color.grey;
						GUI.color = new Color(0.65f, 0.66f, 0.65f);// Color.grey;
					}
				}

				if (i == platformIndex)
				{
					if (!GUILayout.Toggle(true, NativePlugin.PlatformNames[i], GUI.skin.button))
					{
						platformIndex = -1;
					}
				}
				else
				{
					if (GUILayout.Button(NativePlugin.PlatformNames[i]))
					{
						platformIndex = i;
					}
				}
				if ((i+1) % 3 == 0)
				{
					rowCount--;
					GUILayout.EndHorizontal();
				}
				GUI.backgroundColor = Color.white;
				GUI.contentColor = Color.white;
				GUI.color = Color.white;
			}

			if (rowCount > 0)
			{
				GUILayout.EndHorizontal();
			}

			if (platformIndex != (int)_selectedPlatform)
			{
				_selectedPlatform = (NativePlugin.Platform)platformIndex;

				// We do this to clear the focus, otherwise a focused text field will not change when the Toolbar index changes
				EditorGUI.FocusTextInControl("ClearFocus");
			}
		}

		private void EndPlatformSelection()
		{
			GUILayout.EndVertical();
		}

		protected virtual void GUI_Misc()
		{
			EditorGUILayout.PropertyField(_propAllowVsyncDisable);
			EditorGUILayout.PropertyField(_propWaitForEndOfFrame);
			EditorGUILayout.PropertyField(_propSupportTextureRecreate, new GUIContent("Support Texture Recreate", "Using this option will slow rendering (forces GPU sync), but is needed to handle cases where texture resources are recreated, due to alt-tab or window resizing."));
			EditorGUILayout.PropertyField(_propListCodecsOnStart);
			EditorGUILayout.PropertyField(_propPersistAcrossSceneLoads);
			#if AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
			EditorGUILayout.PropertyField(_propTimelineController);
			#endif

			BeginPlatformSelection();
			if (_selectedPlatform == NativePlugin.Platform.Windows)
			{
				EditorGUILayout.PropertyField(_propForceGpuFlush);
				EditorGUILayout.PropertyField(_propMinimumDiskSpaceMB);
			}
			EndPlatformSelection();
		}

		protected virtual void GUI_About()
		{
			CaptureEditorWindow.DrawConfigGUI_About();
		}

		protected void GUI_Visual()
		{
			EditorGUILayout.PropertyField(_propDownScale);
			if (_propDownScale.enumValueIndex == 5)
			{
				EditorGUILayout.PropertyField(_propMaxVideoSize, new GUIContent("Size"));
				_propMaxVideoSize.vector2Value = new Vector2(Mathf.Clamp((int)_propMaxVideoSize.vector2Value.x, 1, NativePlugin.MaxRenderWidth), Mathf.Clamp((int)_propMaxVideoSize.vector2Value.y, 1, NativePlugin.MaxRenderHeight));
			}
			GUILayout.BeginHorizontal();
			EditorGUILayout.PropertyField(_propFrameRate, GUILayout.ExpandWidth(false));
			_propFrameRate.floatValue = Mathf.Clamp(_propFrameRate.floatValue, 0.01f, 240f);
			EditorUtils.FloatAsPopup("▶", "Common Frame Rates", this.serializedObject, _propFrameRate, EditorUtils.CommonFrameRateNames, EditorUtils.CommonFrameRateValues);
			GUILayout.EndHorizontal();

			EditorGUI.BeginDisabledGroup(!_propIsRealtime.boolValue);
			EditorGUILayout.PropertyField(_propTimelapseScale);
			_propTimelapseScale.intValue = Mathf.Max(1, _propTimelapseScale.intValue);
			EditorGUI.EndDisabledGroup();

			EditorGUILayout.PropertyField(_propFlipVertically);
			EditorGUILayout.PropertyField(_propSupportAlpha);

			EditorGUILayout.Space();

			EditorGUI.BeginDisabledGroup(_propOutputType.enumValueIndex != (int)CaptureBase.OutputType.VideoFile);
			GUILayout.Label("Codecs", EditorStyles.boldLabel);
			if (_propOutputType.enumValueIndex == (int)CaptureBase.OutputType.VideoFile)
			{
				GUI_VisualCodecs();
			}
			else
			{
				GUI.color = Color.yellow;
				GUILayout.TextArea("Codec selection only available when video file output");
				GUI.color = Color.white;
			}
			EditorGUI.EndDisabledGroup();

			EditorGUILayout.Space();

			EditorGUI.BeginDisabledGroup(_propIsRealtime.boolValue);
			GUILayout.Label("Motion Blur", EditorStyles.boldLabel);
			if (_propIsRealtime.boolValue)
			{
				GUI.color = Color.yellow;
				GUILayout.TextArea("Motion Blur only available in Offline Render mode");
				GUI.color = Color.white;
			}
			else
			{
				GUI_MotionBlur();
			}
			EditorGUI.EndDisabledGroup();
		}

		protected void GUI_VisualCodecs()
		{
			BeginPlatformSelection();
			if (_selectedPlatform == NativePlugin.Platform.Windows)
			{
				EditorGUILayout.LabelField("Media Foundation");
				EditorGUI.indentLevel++;
				EditorGUILayout.PropertyField(_propUseMediaFoundationH264, new GUIContent("Use MF H.264 MP4"));
				/*EditorGUILayout.PropertyField(_propUseMediaFoundationH265, new GUIContent("Use MF H.265 MP4"));
				if (_propUseMediaFoundationH264.boolValue)
				{
					EditorGUILayout.PropertyField(_propUseMediaFoundationH264, new GUIContent("Hardware Encoding"));
				}*/
				EditorGUI.indentLevel--;
				EditorGUILayout.Separator();

				if (!_propUseMediaFoundationH264.boolValue)
				{
					EditorGUILayout.LabelField("DirectShow");
					EditorGUI.indentLevel++;
					bool searchByName = (_propForceVideoCodecIndexWindows.intValue < 0);
					bool newSearchByName = EditorGUILayout.Toggle("Search by name", searchByName);
					if (searchByName != newSearchByName)
					{
						if (newSearchByName)
						{
							_propForceVideoCodecIndexWindows.intValue = -1;
						}
						else
						{
							_propForceVideoCodecIndexWindows.intValue = 0;
						}
					}

					if (_propForceVideoCodecIndexWindows.intValue < 0)
					{
						EditorGUILayout.PropertyField(_propVideoCodecPriorityWindows, new GUIContent("Codec Search Prority"), true);
					}
					else
					{
						EditorGUILayout.PropertyField(_propForceVideoCodecIndexWindows);
					}
					EditorGUI.indentLevel--;
				}
			}
			else if (_selectedPlatform == NativePlugin.Platform.macOS)
			{
				bool searchByName = (_propForceVideoCodecIndexMacOS.intValue < 0);
				bool newSearchByName = EditorGUILayout.Toggle("Search by name", searchByName);
				if (searchByName != newSearchByName)
				{
					if (newSearchByName)
					{
						_propForceVideoCodecIndexMacOS.intValue = -1;
					}
					else
					{
						_propForceVideoCodecIndexMacOS.intValue = 0;
					}
				}

				if (_propForceVideoCodecIndexMacOS.intValue < 0)
				{
					EditorGUILayout.PropertyField(_propVideoCodecPriorityMacOS, new GUIContent("Codec Search Prority"), true);
				}
				else
				{
					string[] options = { "H264", "HEVC", "MJPEG", "ProRes 4:2:2", "ProRes 4:4:4:4" };
					int[] values = { 0, 1, 2, 3, 4 };
					EditorUtils.IntAsDropdown("", _propForceVideoCodecIndexMacOS, options, values);
				}				
			}
			else if (_selectedPlatform == NativePlugin.Platform.iOS)
			{
				string[] options = { "H264", "HEVC", "MJPEG" };
				int[] values = { 0, 1, 2 };
				EditorUtils.IntAsDropdown("", _propForceVideoCodecIndexIOS, options, values);
			}
			EndPlatformSelection();
		}

		protected void GUI_Audio()
		{
			EditorGUI.BeginDisabledGroup(!_propIsRealtime.boolValue || _propOutputType.enumValueIndex != (int)CaptureBase.OutputType.VideoFile);
			if (!_propIsRealtime.boolValue)
			{
				GUI.color = Color.yellow;
				GUILayout.TextArea("Audio Capture only available in Realtime Capture mode");
				GUI.color = Color.white;
			}
			if (_propOutputType.enumValueIndex != (int)CaptureBase.OutputType.VideoFile)
			{
				GUI.color = Color.yellow;
				GUILayout.TextArea("Audio Capture only available for video file output");
				GUI.color = Color.white;
			}

			if (GUI.enabled)
			{
				_propNoAudio.boolValue = !EditorGUILayout.Toggle("Capture Audio", !_propNoAudio.boolValue);
				if (!_propNoAudio.boolValue)
				{
					EditorUtils.IntAsDropdown("Source", _propForceAudioDeviceIndex, new string[] { "Unity", "System Recording Device" }, new int[] { -1, Mathf.Max(0, _propForceAudioDeviceIndex.intValue) });
					if (_propForceAudioDeviceIndex.intValue >= 0)
					{
						EditorGUILayout.PropertyField(_propForceAudioDeviceIndex);
					}
					else
					{
						EditorGUILayout.PropertyField(_propUnityAudioCapture);
					}
					EditorGUILayout.PropertyField(_propAudioCodecPriority, true);
					EditorGUILayout.PropertyField(_propForceAudioCodecIndex);
				}
			}
			EditorGUI.EndDisabledGroup();
		}

		protected void GUI_Post()
		{
			BeginPlatformSelection();
			if (_selectedPlatform == NativePlugin.Platform.Windows)
			{
				EditorGUILayout.PropertyField(_propPostFastStartMp4, new GUIContent("Streamable MP4"));
			}
			else if ((int)_selectedPlatform >= 0)
			{
				EditorGUI.BeginDisabledGroup(true);
				EditorGUILayout.Toggle(new GUIContent("Streamable MP4"), true);	
				EditorGUI.EndDisabledGroup();
			}
			EndPlatformSelection();
		}

		protected void GUI_MotionBlur()
		{
			EditorGUILayout.PropertyField(_propUseMotionBlur);
			if (_propUseMotionBlur.boolValue)
			{
				EditorGUILayout.PropertyField(_propMotionBlurSamples, new GUIContent("Samples"));
				EditorGUILayout.PropertyField(_propMotionBlurCameras, new GUIContent("Cameras"), true);
			}
		}

		private void LoadSettings()
		{
			_isExpandedStartStop = EditorPrefs.GetBool(SettingsPrefix + "ExpandStartStop", _isExpandedStartStop);
			_isExpandedOutput = EditorPrefs.GetBool(SettingsPrefix + "ExpandOutput", _isExpandedOutput);
			_isExpandedVisual = EditorPrefs.GetBool(SettingsPrefix + "ExpandVisual", _isExpandedVisual);
			_isExpandedAudio = EditorPrefs.GetBool(SettingsPrefix + "ExpandAudio", _isExpandedAudio);
			_isExpandedPost = EditorPrefs.GetBool(SettingsPrefix + "ExpandPost", _isExpandedPost);
			_isExpandedMisc = EditorPrefs.GetBool(SettingsPrefix + "ExpandMisc", _isExpandedMisc);
			_selectedPlatform = (NativePlugin.Platform)EditorPrefs.GetInt(SettingsPrefix + "SelectedPlatform", (int)_selectedPlatform);
		}

		private void SaveSettings()
		{
			EditorPrefs.SetBool(SettingsPrefix + "ExpandStartStop", _isExpandedStartStop);
			EditorPrefs.SetBool(SettingsPrefix + "ExpandOutput", _isExpandedOutput);
			EditorPrefs.SetBool(SettingsPrefix + "ExpandVisual", _isExpandedVisual);
			EditorPrefs.SetBool(SettingsPrefix + "ExpandAudio", _isExpandedAudio);
			EditorPrefs.SetBool(SettingsPrefix + "ExpandPost", _isExpandedPost);
			EditorPrefs.SetBool(SettingsPrefix + "ExpandMisc", _isExpandedMisc);
			EditorPrefs.SetInt(SettingsPrefix + "SelectedPlatform", (int)_selectedPlatform);
		}

		protected virtual void OnEnable()
		{
			#if UNITY_EDITOR_WIN
			_selectedPlatform = NativePlugin.Platform.Windows;
			#elif UNITY_EDITOR_OSX
			_selectedPlatform = NativePlugin.Platform.macOS;
			#endif

			LoadSettings();

			_baseCapture = (CaptureBase)this.target;

			_propCaptureKey = serializedObject.FindProperty("_captureKey");
			_propListCodecsOnStart = serializedObject.FindProperty("_listVideoCodecsOnStart");
			_propPersistAcrossSceneLoads = serializedObject.FindProperty("_persistAcrossSceneLoads");
			_propIsRealtime = serializedObject.FindProperty("_isRealTime");
			_propMinimumDiskSpaceMB = serializedObject.FindProperty("_minimumDiskSpaceMB");

			_propOutputType = serializedObject.FindProperty("_outputType");
			_propImageSequenceFormatWindows = serializedObject.FindProperty("_imageSequenceFormatWindows");
			_propImageSequenceFormatMacOS = serializedObject.FindProperty("_imageSequenceFormatMacOS");
			_propImageSequenceFormatIOS = serializedObject.FindProperty("_imageSequenceFormatIOS");
			_propImageSequenceStartFrame = serializedObject.FindProperty("_imageSequenceStartFrame");
			_propImageSequenceZeroDigits = serializedObject.FindProperty("_imageSequenceZeroDigits");
			_propOutputFolderType = serializedObject.FindProperty("_outputFolderType");
			_propOutputFolderPath = serializedObject.FindProperty("_outputFolderPath");
			_propAppendFilenameTimestamp = serializedObject.FindProperty("_appendFilenameTimestamp");
			_propFileNamePrefix = serializedObject.FindProperty("_filenamePrefix");
			_propAllowManualFileExtension = serializedObject.FindProperty("_allowManualFileExtension");
			_propFileNameExtension = serializedObject.FindProperty("_filenameExtension");
			_propNamedPipePath = serializedObject.FindProperty("_namedPipePath");

			_propUseMediaFoundationH264 = serializedObject.FindProperty("_useMediaFoundationH264");
			_propVideoCodecPriorityWindows = serializedObject.FindProperty("_videoCodecPriorityWindows");
			_propVideoCodecPriorityMacOS = serializedObject.FindProperty("_videoCodecPriorityMacOS");
			_propForceVideoCodecIndexWindows = serializedObject.FindProperty("_forceVideoCodecIndexWindows");
			_propForceVideoCodecIndexMacOS = serializedObject.FindProperty("_forceVideoCodecIndexMacOS");
			_propForceVideoCodecIndexIOS = serializedObject.FindProperty("_forceVideoCodecIndexIOS");

			_propAudioCodecPriority = serializedObject.FindProperty("_audioCodecPriority");
			_propForceAudioCodecIndex = serializedObject.FindProperty("_forceAudioCodecIndex");
			_propForceAudioDeviceIndex = serializedObject.FindProperty("_forceAudioDeviceIndex");
			_propNoAudio = serializedObject.FindProperty("_noAudio");
			_propUnityAudioCapture = serializedObject.FindProperty("_audioCapture");

			_propDownScale = serializedObject.FindProperty("_downScale");
			_propMaxVideoSize = serializedObject.FindProperty("_maxVideoSize");
			_propFrameRate = serializedObject.FindProperty("_frameRate");
			_propTimelapseScale = serializedObject.FindProperty("_timelapseScale");
			_propFlipVertically = serializedObject.FindProperty("_flipVertically");
			_propSupportAlpha = serializedObject.FindProperty("_supportAlpha");
			_propForceGpuFlush = serializedObject.FindProperty("_forceGpuFlush");
			_propWaitForEndOfFrame = serializedObject.FindProperty("_useWaitForEndOfFrame");

			_propUseMotionBlur = serializedObject.FindProperty("_useMotionBlur");
			_propMotionBlurSamples = serializedObject.FindProperty("_motionBlurSamples");
			_propMotionBlurCameras = serializedObject.FindProperty("_motionBlurCameras");

			_propStartTrigger = serializedObject.FindProperty("_startTrigger");
			_propStartDelay = serializedObject.FindProperty("_startDelay");
			_propStartDelaySeconds = serializedObject.FindProperty("_startDelaySeconds");

			_propStopMode = serializedObject.FindProperty("_stopMode");
			_propStopFrames = serializedObject.FindProperty("_stopFrames");
			_propStopSeconds = serializedObject.FindProperty("_stopSeconds");

			_propPostFastStartMp4 = serializedObject.FindProperty("_postCaptureSettings.windows.writeFastStartStreamingForMp4");

			_propAllowVsyncDisable = serializedObject.FindProperty("_allowVSyncDisable");
			_propSupportTextureRecreate = serializedObject.FindProperty("_supportTextureRecreate");

			#if AVPRO_MOVIECAPTURE_PLAYABLES_SUPPORT
			_propTimelineController = serializedObject.FindProperty("_timelineController");
			#endif

			_isTrialVersion = false;
			if (Application.isPlaying)
			{
				_isTrialVersion = IsTrialVersion();
			}
		}

		private void OnDisable()
		{
			SaveSettings();
		}

		protected static bool IsTrialVersion()
		{
			bool result = false;
			try
			{
				result = NativePlugin.IsTrialVersion();
			}
			catch (System.DllNotFoundException)
			{
				// Silent catch as we report this error elsewhere
			}
			return result;
		}

		protected static void ShowNoticeBox(MessageType messageType, string message)
		{
			//GUI.backgroundColor = Color.yellow;
			//EditorGUILayout.HelpBox(message, messageType);

			switch (messageType)
			{
				case MessageType.Error:
					GUI.color = Color.red;
					message = "Error: " + message;
					break;
				case MessageType.Warning:
					GUI.color = Color.yellow;
					message = "Warning: " + message;
					break;
			}

			//GUI.color = Color.yellow;
			GUILayout.TextArea(message);
			GUI.color = Color.white;
		}

		public override bool RequiresConstantRepaint()
		{
			CaptureBase capture = (this.target) as CaptureBase;
			return (Application.isPlaying && capture.isActiveAndEnabled && capture.IsCapturing() && !capture.IsPaused());
		}
	}
}
#endif