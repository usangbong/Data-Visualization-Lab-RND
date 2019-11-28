using UnityEngine;
using UnityEditor;
using UltimateReplay.Storage;
using UltimateReplay.Core;

namespace UltimateReplay.Editor
{
    [CustomEditor(typeof(ReplayMemoryTarget))]
    public class ReplayMemoryTargetEditor : UnityEditor.Editor
    {
        // Properties
        private ReplayMemoryTarget Replay
        {
            get { return target as ReplayMemoryTarget; }
        }

        // Methods
        public override void OnInspectorGUI()
        {
            // Draw the default inspector
            base.OnInspectorGUI();

            GUILayout.Space(10);

            // Calculate the size that this target requires
            int size = CalculateMemoryBufferSize();

            // Show help
            EditorGUILayout.HelpBox(string.Format("This memory target uses approximatley '{0}' {1} for internal buffering (Based on scene samples and record settings)", ReplayHelper.GetMemorySize(size), ReplayHelper.GetMemoryUnitName(size)), MessageType.Info);
        }

        private int CalculateMemoryBufferSize()
        {
            int requiredBytes = 0;

            // Create a temp storage container
            ReplayState state = new ReplayState();

            // Get all active components
            foreach(ReplayBehaviour replay in Component.FindObjectsOfType<ReplayBehaviour>())
            {
                // Calculate the required size
                replay.OnReplaySerialize(state);
            }

            // Multiply by record fps
            ReplayManager manager = Component.FindObjectOfType<ReplayManager>();

            // Default to 24 fps
            requiredBytes = (manager != null) ? state.Size * manager.recordFPS : state.Size * 24;

            // Take into account the number of seconds in the memory buffer
            requiredBytes = (int)(requiredBytes * Replay.recordSeconds);

            return requiredBytes;
        }
    }
}
