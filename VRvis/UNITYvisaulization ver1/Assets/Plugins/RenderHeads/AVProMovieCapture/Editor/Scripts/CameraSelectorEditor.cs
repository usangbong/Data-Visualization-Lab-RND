#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;

//-----------------------------------------------------------------------------
// Copyright 2012-2020 RenderHeads Ltd.  All rights reserved.
//-----------------------------------------------------------------------------

namespace RenderHeads.Media.AVProMovieCapture.Editor
{
	[CanEditMultipleObjects]
	[CustomEditor(typeof(CameraSelector))]
	public class CameraSelectorEditor : UnityEditor.Editor
	{
		private SerializedProperty _propSelectBy;
		private SerializedProperty _propScanFrequency;
		private SerializedProperty _propScanHiddenCameras;
		private SerializedProperty _propTag;
		private SerializedProperty _propName;
		private SerializedProperty _propCamera;

		void OnEnable()
		{
			_propSelectBy = serializedObject.FindProperty("_selectBy");
			_propScanFrequency = serializedObject.FindProperty("_scanFrequency");
			_propScanHiddenCameras = serializedObject.FindProperty("_scanHiddenCameras");
			_propTag = serializedObject.FindProperty("_tag");
			_propName = serializedObject.FindProperty("_name");
			_propCamera = serializedObject.FindProperty("_camera");
		}

		public override void OnInspectorGUI()
		{
			serializedObject.Update();

			EditorGUILayout.PropertyField(_propScanFrequency);
			EditorGUILayout.PropertyField(_propScanHiddenCameras);
			EditorGUILayout.PropertyField(_propSelectBy);
			if (_propSelectBy.enumValueIndex == (int)CameraSelector.SelectByMode.Name)
			{
				EditorGUILayout.PropertyField(_propName);
			}
			else if (_propSelectBy.enumValueIndex == (int)CameraSelector.SelectByMode.Tag)
			{
				EditorGUILayout.PropertyField(_propTag);
			}
			else if (_propSelectBy.enumValueIndex == (int)CameraSelector.SelectByMode.Manual)
			{
				EditorGUILayout.PropertyField(_propCamera);
			}
			if (Application.isPlaying)
			{
				EditorGUILayout.Separator();

				GUILayout.Label("Cameras:");

				CameraSelector selector = (this.target) as CameraSelector;

				// Display buttons for all possible cameras
				for (int i = 0; i < selector.CameraCacheCount; i++)
				{
					if (selector.Camera != selector.CameraCache[i])
					{
						if (GUILayout.Button(selector.CameraCache[i].name))
						{
							selector.Camera = selector.CameraCache[i];
						}
					}
					else
					{
						GUI.color = Color.green;
						GUILayout.Button(selector.Camera.name);
						GUI.color = Color.white;
					}
				}

				EditorGUILayout.Separator();
				if (_propScanFrequency.enumValueIndex != (int)CameraSelector.ScanFrequencyMode.Frame)
				{
					if (GUILayout.Button("Update Camera List"))
					{
						selector.UpdateCameraCache();
					}
				}
			}

			serializedObject.ApplyModifiedProperties();
		}
	}
}
#endif