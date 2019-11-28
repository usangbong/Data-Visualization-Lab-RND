using UnityEngine;

namespace UltimateReplay.Demo
{
    /// <summary>
    /// A script using in the audio demo to show the <see cref="ReplayAudio"/> component working. 
    /// </summary>
    public class AudioDemo : MonoBehaviour
    {
        // Public
        /// <summary>
        /// The <see cref="ReplayAudio"/> script.
        /// </summary>
        public ReplayAudio replayAudio;

        // Methods
        /// <summary>
        /// Called by Unity.
        /// </summary>
        public void Update()
        {
            // Check for unassigned audio
            if (replayAudio == null)
                return;

            // Check for play
            if(Input.GetKeyDown(KeyCode.Space) == true)
            {
                // Play the audio
                replayAudio.Play();
            }
        }

        /// <summary>
        /// Called by Unity.
        /// </summary>
        public void OnGUI()
        {
            GUILayout.BeginArea(new Rect(0, 0, Screen.width, Screen.height));
            {
                GUILayout.FlexibleSpace();

                GUILayout.BeginHorizontal();
                {
                    GUILayout.FlexibleSpace();

                    GUILayout.Label("Replay Audio Demo - ");
                    GUILayout.Label("Press 'Space' to play audio effect");

                    GUILayout.FlexibleSpace();
                }
                GUILayout.EndHorizontal();
            }
            GUILayout.EndArea();
        }
    }
}
