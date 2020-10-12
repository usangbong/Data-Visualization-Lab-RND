using UnityEngine;
using UnityEngine.SceneManagement;

//-----------------------------------------------------------------------------
// Copyright 2012-2020 RenderHeads Ltd.  All rights reserved.
//-----------------------------------------------------------------------------

namespace RenderHeads.Media.AVProMovieCapture
{
	/// <summary>
	/// Selects the camera to use for captures based on various factors
	/// TODO: add support for persisting across scene changes
	/// </summary>
	[AddComponentMenu("AVPro Movie Capture/Camera Selector", 300)]
	public class CameraSelector : MonoBehaviour
	{
		public enum SelectByMode
		{
			HighestDepthCamera,
			MainCameraTag,
			Tag,
			Name,
			Manual,
		}

		public enum ScanFrequencyMode
		{
			Manual,
			SceneLoad,
			Frame,
		}

		[SerializeField] SelectByMode _selectBy = SelectByMode.HighestDepthCamera;
		[SerializeField] ScanFrequencyMode _scanFrequency = ScanFrequencyMode.SceneLoad;
		[SerializeField] bool _scanHiddenCameras = false;
		[SerializeField] string _tag = "MainCamera";
		[SerializeField] string _name = "Main Camera";
		[SerializeField] Camera _camera = null;

		private Camera[] _cameraCache = new Camera[0];
		private int _cameraCount;
		private int _cameraCacheFrame = -1;

#if UNITY_EDITOR
		public int CameraCacheCount
		{
			get { return _cameraCount; }
		}
		public Camera[] CameraCache
		{
			get { return _cameraCache; }
		}
#endif

		public Camera Camera
		{
			get { return _camera; }
			set { _camera = value; _selectBy = SelectByMode.Manual; }
		}

		public SelectByMode SelectBy
		{
			get { return _selectBy; }
			set { _selectBy = value; }
		}

		public ScanFrequencyMode ScanFrequency
		{
			get { return _scanFrequency; }
			set { _scanFrequency = value; ResetSceneLoading(); }
		}

		public bool ScanHiddenCameras
		{
			get { return _scanHiddenCameras; }
			set { _scanHiddenCameras = value; }
		}

		public string SelectTag
		{
			get { return _tag; }
			set { _tag = value; }
		}

		public string SelectName
		{
			get { return _name; }
			set { _name = value; }
		}		

		void Awake()
		{
			ResetSceneLoading();
		}

		void Start()
		{
			ScanForCameraChange();
		}

		void OnValidate()
		{
			ResetSceneLoading();
		}

		void Update()
		{
			if (_scanFrequency == ScanFrequencyMode.Frame)
			{
				ScanForCameraChange();
			}
		}

		void OnDestroy()
		{
			SceneManager.sceneLoaded -= OnSceneLoaded;
		}		

		void ResetSceneLoading()
		{
			SceneManager.sceneLoaded -= OnSceneLoaded;
			if (_scanFrequency == ScanFrequencyMode.SceneLoad)
			{
				SceneManager.sceneLoaded += OnSceneLoaded;
			}
		}
		
		void OnSceneLoaded(Scene scene, LoadSceneMode mode)
		{
			if (_scanFrequency == ScanFrequencyMode.SceneLoad)
			{
				ScanForCameraChange();
			}
		}

		public bool ScanForCameraChange()
		{
			bool result = false;
			Camera camera = FindCamera();
			if (_camera != camera)
			{
				_camera = camera;
				if (_camera != null)
				{
					//Debug.Log("Camera " + _camera.name);
				}
				result = true;
			}
			return result;
		}

		Camera FindCamera()
		{
			Camera result = null;
			switch (_selectBy)
			{
				case SelectByMode.HighestDepthCamera:
					UpdateCameraCache();
					result = FindCameraByHighestDepth(_cameraCount, _cameraCache);
					break;
				case SelectByMode.MainCameraTag:
					result = Camera.main;
					break;
				case SelectByMode.Tag:
					UpdateCameraCache();
					result = FindCameraByTag(_cameraCount, _cameraCache, _tag);
					break;
				case SelectByMode.Name:
					UpdateCameraCache();
					result = FindCameraByName(_cameraCount, _cameraCache, _name);
					break;
				case SelectByMode.Manual:
					result = _camera;
					break;
			}
			return result;
		}

		public void UpdateCameraCache()
		{
			// Prevent multiple scans per frame
			if (Time.frameCount == _cameraCacheFrame) return;

			if (!_scanHiddenCameras)
			{
				// FAST - list active cameras
				if (_cameraCache.Length < Camera.allCamerasCount)
				{
					_cameraCache = new Camera[Camera.allCamerasCount];
					
				}
				_cameraCount = Camera.GetAllCameras(_cameraCache);
			}
			else
			{
				// SLOW - list all cameras
				_cameraCache = Resources.FindObjectsOfTypeAll<Camera>();
				_cameraCount = _cameraCache.Length;
			}

			_cameraCacheFrame = Time.frameCount;
		}

		static Camera FindCameraByHighestDepth(int cameraCount, Camera[] cameras)
		{
			Camera result = null;
			float maxDepth = float.MinValue;
			for (int i = 0; i < cameraCount; i++)
			{
				Camera c = cameras[i];
				if (result == null || c.depth > maxDepth)
				{
					result = c;
					maxDepth = c.depth;
				}
			}
			return result;
		}

		static Camera FindCameraByTag(int cameraCount, Camera[] cameras, string tag)
		{
			Camera result = null;
			for (int i = 0; i < cameraCount; i++)
			{
				Camera c = cameras[i];
				if (c.CompareTag(tag))
				{
					result = c;
					break;
				}
			}
			return result;
		}

		static Camera FindCameraByName(int cameraCount, Camera[] cameras, string name)
		{
			Camera result = null;
			for (int i = 0; i < cameraCount; i++)
			{
				Camera c = cameras[i];
				if (c.name == name)
				{
					result = c;
					break;
				}
			}
			return result;
		}
	}
}