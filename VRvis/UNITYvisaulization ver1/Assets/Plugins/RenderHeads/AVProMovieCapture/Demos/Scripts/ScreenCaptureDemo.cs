using UnityEngine;
using System.Collections.Generic;

//-----------------------------------------------------------------------------
// Copyright 2012-2019 RenderHeads Ltd.  All rights reserved.
//-----------------------------------------------------------------------------

namespace RenderHeads.Media.AVProMovieCapture.Demos
{
	public class ScreenCaptureDemo : MonoBehaviour
	{
		[SerializeField]
		private AudioClip _audioBG = null;

		[SerializeField]
		private AudioClip _audioHit = null;

		[SerializeField]
		private float _speed = 1.0f;

		[SerializeField]
		private CaptureBase _capture = null;

		[SerializeField]
		private GUISkin _guiSkin = null;

		[SerializeField]
		private bool _spinCamera = true;

		private List<FileWritingHandler> _fileWritingHandlers = new List<FileWritingHandler>(4);

		// State
		private float _timer;

		private void Start()
		{
			// Play music track
			if (_audioBG != null)
			{
				AudioSource.PlayClipAtPoint(_audioBG, Vector3.zero);
			}
			if (_capture != null)
			{
				_capture.FileWritingAction += OnFileWriting;
			}
		}

		private void OnFileWriting(FileWritingHandler handler)
		{
			_fileWritingHandlers.Add(handler);
		}

		private void Update()
		{
			// Press the S key to trigger audio and background color change - useful for testing A/V sync
			if (Input.GetKeyDown(KeyCode.S))
			{
				if (_audioHit != null && _capture != null && _capture.IsCapturing())
				{
					AudioSource.PlayClipAtPoint(_audioHit, Vector3.zero);
					Camera.main.backgroundColor = new Color(Random.value, Random.value, Random.value, 0);
				}
			}

			// ESC to stop capture and quit
			if (Input.GetKeyDown(KeyCode.Escape))
			{
				if (_capture != null && _capture.IsCapturing())
				{
					_capture.StopCapture();
				}
				else
				{
					Application.Quit();
				}
			}

			// Spin the camera around
			if (_spinCamera && Camera.main != null)
			{
				Camera.main.transform.RotateAround(Vector3.zero, Vector3.up, 20f * Time.deltaTime * _speed);
			}

			for (int i = _fileWritingHandlers.Count - 1; i >= 0; i--)
			{
				FileWritingHandler handler = _fileWritingHandlers[i];
				if (handler.IsFileReady())
				{
					Debug.Log("File is ready: " + handler.Path);
					_fileWritingHandlers.RemoveAt(i);
				}
			}
		}

		void OnDestroy()
		{
			foreach (FileWritingHandler handler in _fileWritingHandlers)
			{
				handler.Dispose();
			}
		}

		private void OnGUI()
		{
			GUI.skin = _guiSkin;
			Rect r = new Rect(Screen.width - 108, 64, 128, 28);
			GUI.Label(r, "Frame " + Time.frameCount);
		}
	}
}