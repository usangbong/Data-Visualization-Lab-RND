#if UNITY_2017_1_OR_NEWER
using UnityEngine;
using System.Collections.Generic;
using UnityEngine.SceneManagement;
using UnityEngine.Playables;

//-----------------------------------------------------------------------------
// Copyright 2012-2020 RenderHeads Ltd.  All rights reserved.
//-----------------------------------------------------------------------------

namespace RenderHeads.Media.AVProMovieCapture
{
	/// <summary>
	/// Controls timeline updates time during offline captures
	/// </summary>
	[AddComponentMenu("AVPro Movie Capture/Timeline Controller", 300)]
	public class TimelineController : MonoBehaviour
	{
		public enum ScanFrequencyMode
		{
			SceneLoad,
			Frame,
		}

		[SerializeField] ScanFrequencyMode _scanFrequency = ScanFrequencyMode.SceneLoad;

		public ScanFrequencyMode ScanFrequency
		{
			get { return _scanFrequency; }
			set { _scanFrequency = value; ResetSceneLoading(); }
		}

		internal class TimelineInstance
		{
			private PlayableDirector	_director					= null;
			private DirectorUpdateMode	_originalTimeUpdateMode		= DirectorUpdateMode.DSPClock;
			private bool				_isControlling				= false;
			private bool				_isCapturing				= false;

			internal TimelineInstance(PlayableDirector director)
			{
				_director = director;
			}

			internal bool Is(PlayableDirector director)
			{
				return (_director == director);
			}

			internal void StartCapture()
			{
				// First capture to touch the playable directors
				if (!_isCapturing)
				{
					// Null check in case director no longer exists
					if (_director != null)
					{
						// Want to manually update?
						// TODO: should we include ALL directors, as they may switch from manual to something else later on?
						_isControlling = (_director.timeUpdateMode != DirectorUpdateMode.Manual);

						if (_isControlling)
						{
							// Cache original update mode
							_originalTimeUpdateMode = _director.timeUpdateMode;

							bool wasPlaying = _director.state == PlayState.Playing;

							// Set to manual update mode
							// NOTE: Prior to Unity 2018.2 changing from DSP Clock to Manual did nothing, as DSP Clock mode was set to ignore manual updates
							_director.timeUpdateMode = DirectorUpdateMode.Manual;
							
							// NOTE: In newer versions of Unity (post 2018.2) changing the timeUpdateMode to Manual pauses playback, so we must resume it
							if (wasPlaying && _director.state == PlayState.Paused)
							{
								_director.Resume();
							}
						}
					}
					_isCapturing = true;
				}
			}

			internal void Update(float deltaTime)
			{
				if (_isControlling && _isCapturing)
				{
					if (_director != null && _director.isActiveAndEnabled)
					{
						if (_director.state == PlayState.Playing)
						{
							double time = _director.time + deltaTime;
							if (time < _director.duration)
							{
								_director.time = time;
								_director.Evaluate();
							}
							else
							{
								switch (_director.extrapolationMode)
								{
									case DirectorWrapMode.Loop:
										_director.time = time % _director.duration;
										_director.Evaluate();
										break;
									case DirectorWrapMode.Hold:
										_director.time = _director.duration;
										_director.Evaluate();
										break;
									case DirectorWrapMode.None:
										_director.time = 0f;
										_director.Pause();
										break;
								}
							}
						}
					}
				}
			}

			internal void StopCapture()
			{
				if (_isCapturing)
				{
					// TODO: what happens to the director when the scene is unloaded?
					if (_director != null)
					{
						// We were controlling?
						if (_isControlling)
						{
							bool wasPlaying = (_director.state == PlayState.Playing);

							// Revert update mode to original
							_director.timeUpdateMode = _originalTimeUpdateMode;

							if (wasPlaying)
							{
								// Timeline seems to get paused after changing play mode (in some versions of Unity), only a pause and resume keeps it going
								_director.Pause();
								_director.Resume();
							}
							_isControlling = false;
						}
					}
					_isCapturing = false;
				}
			}
		}

		private List<TimelineInstance>	_timelines	= new List<TimelineInstance>(8);

		void Awake()
		{
			ResetSceneLoading();
		}

		void OnValidate()
		{
			ResetSceneLoading();
		}

		internal void UpdateFrame()
		{
			if (_scanFrequency == ScanFrequencyMode.Frame)
			{
				ScanForPlayableDirectors();
			}
			foreach (TimelineInstance timeline in _timelines)
			{
				timeline.Update(Time.deltaTime);
			}
		}

		internal void StartCapture()
		{
			ScanForPlayableDirectors();
			foreach (TimelineInstance timeline in _timelines)
			{
				timeline.StartCapture();
			}
		}

		internal void StopCapture()
		{
			foreach (TimelineInstance timeline in _timelines)
			{
				timeline.StopCapture();
			}
		}

		public void ScanForPlayableDirectors()
		{
			// Remove any timeline instances with deleted (null) directors
			for (int i = 0; i < _timelines.Count; i++)
			{
				TimelineInstance timeline = _timelines[i];
				if (timeline.Is(null))
				{
					_timelines.RemoveAt(i); i--;
				}
			}

			// Find all inactive and active directors
			PlayableDirector[] directors = Resources.FindObjectsOfTypeAll<PlayableDirector>();

			// Create a unique instance for each director
			foreach (PlayableDirector playableDirector in directors)
			{
				// Check we don't already have this director
				bool hasDirector = false;
				foreach (TimelineInstance timeline in _timelines)
				{
					if (timeline.Is(playableDirector))
					{
						hasDirector = true;
						break;
					}
				}

				// Add to the list
				if (!hasDirector)
				{
					_timelines.Add(new TimelineInstance(playableDirector));
				}
			}
		}

		void OnDestroy()
		{
			SceneManager.sceneLoaded -= OnSceneLoaded;
			StopCapture();
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
				ScanForPlayableDirectors();
			}
		}
	}
}
#endif