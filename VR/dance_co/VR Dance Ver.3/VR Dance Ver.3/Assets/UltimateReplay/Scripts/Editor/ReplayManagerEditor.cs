using UnityEngine;
using UnityEditor;
using UltimateReplay.Core;
using System.Collections.Generic;
using System.Text;

namespace UltimateReplay.Editor
{
    [CustomEditor(typeof(ReplayManager))]
    public class ReplayManagerEditor : UnityEditor.Editor
    {
        public override void OnInspectorGUI()
        {
            base.OnInspectorGUI();

            // Display prefab list error if necesary
            DisplayPrefabErrors();

            GUILayout.Space(10);

            // Calculate required buffer size
            int sampleSize = CalculateSampleSize();
            int frameSize = CalculateFrameSize();

            EditorGUILayout.HelpBox(string.Format("All replay objects generate approximatley '{0}' {1} per sample and approximatley '{2}' {3} per second (Based on scene samples and record settings)", ReplayHelper.GetMemorySize(sampleSize), ReplayHelper.GetMemoryUnitName(sampleSize), ReplayHelper.GetMemorySize(frameSize), ReplayHelper.GetMemoryUnitName(frameSize)), MessageType.Info);
        }

        private int CalculateSampleSize()
        {
            // Create a temp storage container
            ReplayState state = new ReplayState();

            // Get all active components
            foreach(ReplayObject replay in Component.FindObjectsOfType<ReplayObject>())
            {
                // Calculate the required size
                replay.OnReplaySerialize(state);
            }

            // Get the full size
            return state.Size;
        }

        private int CalculateFrameSize()
        {
            // Get the replay manager
            ReplayManager manager = (target as ReplayManager);

            // Take record fps into account
            return CalculateSampleSize() * manager.recordFPS;
        }

        private void DisplayPrefabErrors()
        {
            // Get the manager
            ReplayManager manager = target as ReplayManager;

            // Get the list of game objects
            GameObject[] prefabs = manager.prefabs;

            List<GameObject> replayErrors = new List<GameObject>();
            List<GameObject> prefabErrors = new List<GameObject>();

            foreach(GameObject go in prefabs)
            {
                // Check for null preab (Are allowed)
                if (go == null)
                    continue;

                // Try to get component
                ReplayObject obj = go.GetComponent<ReplayObject>();

                // Check for error
                if(obj == null)
                {
                    // Mark an error
                    replayErrors.Add(go);
                    continue;
                }

                // Check for prefab
                if(obj.IsPrefab == false)
                {
                    // Mark a prefab error
                    prefabErrors.Add(go);
                }
            }

            // Display a help box
            if(replayErrors.Count > 0)
            {
                StringBuilder builder = new StringBuilder();

                for(int i = 0; i < replayErrors.Count; i++)
                {
                    // Use the name in the error
                    builder.Append(replayErrors[i].name);

                    // There are more errors left
                    if (i < replayErrors.Count - 1)
                        builder.Append(", ");
                }

                // Display a help box
                EditorGUILayout.HelpBox(string.Format("The following prefabs do not have ReplayObject scripts attached and will be ignored at runtime: {0}", builder.ToString()), MessageType.Error);
            }

            // Display a help box
            if (prefabErrors.Count > 0)
            {
                StringBuilder builder = new StringBuilder();

                for (int i = 0; i < prefabErrors.Count; i++)
                {
                    // Use the name in the error
                    builder.Append(prefabErrors[i].name);

                    // There are more errors left
                    if (i < prefabErrors.Count - 1)
                        builder.Append(", ");
                }

                // Display a help box
                EditorGUILayout.HelpBox(string.Format("The following replay prefabs are not prefab assets and will be ignored at runtime: {0}. Make sure scene prefab instances are not registered", builder.ToString()), MessageType.Error);
            }
        }
    }
}
