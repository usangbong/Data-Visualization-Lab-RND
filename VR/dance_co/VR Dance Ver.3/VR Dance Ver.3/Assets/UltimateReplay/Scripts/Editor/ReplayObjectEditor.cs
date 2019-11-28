using System.Text;
using UnityEngine;
using UnityEditor;

namespace UltimateReplay.Editor
{
    [CustomEditor(typeof(ReplayObject))]
    public class ReplayObjectEditor : UnityEditor.Editor
    {
        // Private
        private static readonly Color light = new Color(0.9f, 0.9f, 0.9f);
        private static readonly Color dark = new Color(0.7f, 0.7f, 0.7f);

        // Properties
        public ReplayObject Replay
        {
            get { return target as ReplayObject; }
        }

        // Methods
        public override void OnInspectorGUI()
        {
            // Draw the default inspector
            base.OnInspectorGUI();

            GUILayout.BeginHorizontal();
            {
                EditorGUILayout.PrefixLabel("Observed Components");

                // Observed components
                GUILayout.BeginVertical(EditorStyles.helpBox);
                {
                    // Call rebuild
                    Replay.RebuildComponentList();

                    GUIStyle labelStyle = new GUIStyle(GUI.skin.label);
                    labelStyle.padding = new RectOffset(0, 0, -2, -2);

                    // Find all child scripts
                    ReplayBehaviour[] all = Replay.GetComponentsInChildren<ReplayBehaviour>(false);

                    // Draw all items
                    for (int i = 0; i < all.Length; i++)
                    {
                        // Select back colour
                        GUI.backgroundColor = (i % 2 == 0) ? light : dark;

                        // Draw a row
                        GUILayout.BeginHorizontal(EditorStyles.helpBox, GUILayout.Height(10));
                        {
                            // Draw a name field
                            GUILayout.Label(string.Format("{0} ({1})", all[i].name, all[i].GetType().Name), labelStyle);

							if(Replay.IsComponentObserved(all[i]) == false)
                            {
                                GUILayout.FlexibleSpace();
                                
                                labelStyle.fontStyle = FontStyle.Bold;
                                GUILayout.Label(new GUIContent("[Not Recorded]", "This component is not recorded because it is marked with the 'ReplayIgnore' attribute"), labelStyle);
                                labelStyle.fontStyle = FontStyle.Normal;
                            }
                        }
                        GUILayout.EndHorizontal();

                        // Negative space
                        GUILayout.Space(-3);
                    }

                    // reset colour
                    GUI.backgroundColor = light;

                    if (all.Length == 0)
                    {
                        GUILayout.BeginHorizontal();
                        {
                            GUILayout.FlexibleSpace();
                            GUILayout.Label("(none)");
                            GUILayout.FlexibleSpace();
                        }
                        GUILayout.EndHorizontal();
                    }
                }
                GUILayout.EndVertical();
            }
            GUILayout.EndHorizontal();

            // Display prefab hint
            if(Replay.IsPrefab == true)
            {
                EditorGUILayout.HelpBox("This replay object is a prefab. You can register this prefab in the Replay Manager inspector so that the object can be dynamically instantiated or destroyed during recording", MessageType.Info);
            }


            // Calcualte the size that the object generates
            int size = CalculateReplaySize();

            if (size != 0)
            {
                GUILayout.Space(10);

                StringBuilder builder = new StringBuilder();

                // Generate size info
                builder.AppendFormat("This replay object generates '{0}' {1} per sample on average", ReplayHelper.GetMemorySize(size), ReplayHelper.GetMemoryUnitName(size));

                // Show help
                EditorGUILayout.HelpBox(builder.ToString(), MessageType.Info);
            }
            else
            {
                // No bytes
                EditorGUILayout.HelpBox("This replay object does not generate any data", MessageType.Info);
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
