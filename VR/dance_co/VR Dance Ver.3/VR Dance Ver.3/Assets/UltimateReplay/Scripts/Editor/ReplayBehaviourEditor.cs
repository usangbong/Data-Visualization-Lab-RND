using System.Text;
using UltimateReplay.Core;
using UnityEditor;
using UnityEngine;

namespace UltimateReplay.Editor
{
    [CustomEditor(typeof(ReplayBehaviour), true)]
    [CanEditMultipleObjects]
    public class ReplayBehaviourEditor : UnityEditor.Editor
    {
        // Properties
        private ReplayBehaviour Replay
        {
            get { return target as ReplayBehaviour; }
        }

        // Methods
        public override void OnInspectorGUI()
        {
            // Draw the default inspector
            base.OnInspectorGUI();

            // Calcualte the size that the object generates
            int size = CalculateReplaySize();

            if (size != 0)
            {
                GUILayout.Space(10);
                
                StringBuilder builder = new StringBuilder();

                // Generate size info
                builder.AppendFormat("This replay component generates '{0}' {1} per sample on average", ReplayHelper.GetMemorySize(size), ReplayHelper.GetMemoryUnitName(size));

                // Show help
                EditorGUILayout.HelpBox(builder.ToString(), MessageType.Info);
            }
            else
            {
                // No bytes
                EditorGUILayout.HelpBox("This replay component does not generate any data", MessageType.Info);
            }
        }

        private int CalculateReplaySize()
        {
            // Create an empty object state
            ReplayState state = new ReplayState();

            // Serialize the object
            Replay.OnReplaySerialize(state);

            // Get the new size of the state
            return state.Size;
        }
    }
}
