using UnityEngine;
using UnityEditor;

using UltimateReplay.Core;

namespace UltimateReplay.Editor
{
    [CustomPropertyDrawer(typeof(ReplayIdentity))]
    public class ReplayIdentityEditor : PropertyDrawer
    {
        // Methods
        public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
        {
            // Begin drawing the property
            EditorGUI.BeginProperty(position, label, property);
            {
                // Draw a background box
                GUI.Box(position, string.Empty, EditorStyles.helpBox);
                
                // Draw the label
                position = EditorGUI.PrefixLabel(position, GUIUtility.GetControlID(FocusType.Passive), label);

                GUI.enabled = false;
                EditorGUI.PropertyField(position, property.FindPropertyRelative("id"), GUIContent.none);
                GUI.enabled = true;
            }
            EditorGUI.EndProperty();
        }
    }
}
