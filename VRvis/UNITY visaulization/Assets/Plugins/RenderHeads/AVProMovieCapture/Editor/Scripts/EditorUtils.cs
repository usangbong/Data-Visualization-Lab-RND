#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System.Reflection;

//-----------------------------------------------------------------------------
// Copyright 2012-2019 RenderHeads Ltd.  All rights reserved.
//-----------------------------------------------------------------------------

namespace RenderHeads.Media.AVProMovieCapture.Editor
{
	/*public static class Utils
	{
		public static T GetCopyOf<T>(this Component comp, T other) where T : Component
		{
			System.Type type = comp.GetType();
			if (type != other.GetType())
			{
				return null; // type mis-match
			}
			BindingFlags flags = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Default | BindingFlags.DeclaredOnly;
			PropertyInfo[] pinfos = type.GetProperties(flags);
			for (int i = 0; i < pinfos.Length; i++)
			{
				PropertyInfo pinfo = pinfos[i];
				if (pinfo.CanWrite)
				{
					try
					{
						pinfo.SetValue(comp, pinfo.GetValue(other, null), null);
					}
					catch { } // In case of NotImplementedException being thrown. For some reason specifying that exception didn't seem to catch it, so I didn't catch anything specific.
				}
			}
			FieldInfo[] finfos = type.GetFields(flags);
			foreach (var finfo in finfos)
			{
				finfo.SetValue(comp, finfo.GetValue(other));
			}
			return comp as T;
		}
	}*/

	public static class EditorUtils
	{
		public static string[] CommonFrameRateNames = { "1", "10", "15", "23.98", "24 - CINEMA", "25 - PAL", "29.97 - NTSC", "30", "50", "59.94", "60", "75", "90", "120" };
		public static float[] CommonFrameRateValues = { 1f, 10f, 15f, 23.976f, 24f, 25f, 29.97f, 30f, 50f, 59.94f, 60f, 75f, 90f, 120f };

		internal static string[] OutputTypeNames = new string[] { "Video File", "Image Sequence", "Named Pipe" };

		public static void CentreLabel(string text, GUIStyle style = null)
		{
			GUILayout.BeginHorizontal();
			GUILayout.FlexibleSpace();
			if (style == null)
			{
				GUILayout.Label(text);
			}
			else
			{
				GUILayout.Label(text, style);
			}
			GUILayout.FlexibleSpace();
			GUILayout.EndHorizontal();
		}

		public static void BoolAsDropdown(string name, SerializedProperty prop, string trueOption, string falseOption)
		{
			string[] popupNames = { trueOption, falseOption };
			int popupIndex = 0;
			if (!prop.boolValue)
			{
				popupIndex = 1;
			}
			popupIndex = EditorGUILayout.Popup(name, popupIndex, popupNames);
			prop.boolValue = (popupIndex == 0);
		}

		public static void EnumAsDropdown(string name, SerializedProperty prop, string[] options)
		{
			prop.enumValueIndex = EditorGUILayout.Popup(name, prop.enumValueIndex, options);
		}

		public static void IntAsDropdown(string name, SerializedProperty prop, string[] options, int[] values)
		{
			int index = 0;
			for (int i = 0; i < values.Length; i++)
			{
				if (values[i] == prop.intValue)
				{
					index = i;
					break;
				}
			}
			index = EditorGUILayout.Popup(name, index, options);
			prop.intValue = values[index];
		}

		public static void FloatAsDropdown(string name, SerializedProperty prop, string[] options, float[] values, bool customAtEnd)
		{
			bool isFound = false;
			int index = 0;
			for (int i = 0; i < values.Length; i++)
			{
				if (values[i] == prop.floatValue)
				{
					isFound = true;
					index = i;
					break;
				}
			}
			if (!isFound && customAtEnd)
			{
				index = options.Length - 1;
			}
			EditorGUI.BeginChangeCheck();
			if (string.IsNullOrEmpty(name))
			{
				index = EditorGUILayout.Popup(index, options);
			}
			else
			{
				index = EditorGUILayout.Popup(name, index, options);
			}
			if (EditorGUI.EndChangeCheck())
			{
				prop.floatValue = values[index];
			}
		}

		private struct FloatPopupData
		{
			public FloatPopupData(SerializedObject obj, SerializedProperty prop, float value, Object target)
			{
				_obj = obj;
				_prop = prop;
				_value = value;
				_target = target;
			}

			public void Apply()
			{
				_prop.floatValue = _value;
				if (_obj.ApplyModifiedProperties())
				{
					EditorUtility.SetDirty(_target);
				}
			}

			private Object _target;
			private SerializedObject _obj;
			private SerializedProperty _prop;
			private float _value;
		}

		private static void FloatAsPopupCallback_Select(object obj)
		{
			((FloatPopupData)obj).Apply();
		}

		public static void FloatAsPopup(string buttonText, string popupText, SerializedObject obj, SerializedProperty prop, string[] options, float[] values)
		{
			if (GUILayout.Button(buttonText, GUILayout.ExpandWidth(false)))
			{
				// Remove focus to clear the selection, otherwise the property field will not update
				GUI.FocusControl(null);

				GenericMenu toolsMenu = new GenericMenu();
				toolsMenu.AddDisabledItem(new GUIContent(popupText));
				toolsMenu.AddSeparator("");
				for (int i = 0; i < options.Length; i++)
				{
					bool isSelected = (values[i] == prop.floatValue);
					toolsMenu.AddItem(new GUIContent(options[i]), isSelected, FloatAsPopupCallback_Select, new FloatPopupData(obj, prop, values[i], obj.targetObject));
				}

				toolsMenu.ShowAsContext();
			}
		}

		public static void DrawSection(string name, ref bool isExpanded, System.Action action)
		{
			Color boxbgColor = new Color(0.8f, 0.8f, 0.8f, 0.1f);
			if (EditorGUIUtility.isProSkin)
			{
				boxbgColor = Color.black;
			}
				DrawSectionColored(name, ref isExpanded, action, boxbgColor, Color.white, Color.white);
		}

		public static void DrawSectionColored(string name, ref bool isExpanded, System.Action action, Color boxbgcolor, Color bgcolor, Color color)
		{
			GUI.color = Color.white;
			GUI.backgroundColor = Color.clear;
			//GUI.backgroundColor = bgcolor;
			if (isExpanded)
			{
				GUI.color = Color.white;
				GUI.backgroundColor = boxbgcolor;
			}

			GUILayout.BeginVertical("box");
			GUI.color = color;
			GUI.backgroundColor = bgcolor;
			
			if (GUILayout.Button(name, EditorStyles.toolbarButton))
			{
				isExpanded = !isExpanded;
			}
			//GUI.backgroundColor = Color.white;
			//GUI.color = Color.white;

			if (isExpanded)
			{
				action.Invoke();
			}

			GUI.backgroundColor = Color.white;
			GUI.color = Color.white;

			GUILayout.EndVertical();
		}
	}
}
#endif