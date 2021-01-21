using System;
using System.Linq.Expressions;
using UnityEditor;
using UnityEngine;

namespace PieChart.ViitorCloud
{
    [CustomEditor(typeof(PieChart))]
    public class PieChart_Editor : Editor
    {
        public override void OnInspectorGUI()
        {
            PieChart script = (PieChart)target;
            EditorGUILayout.Space();
            EditorGUILayout.LabelField("Pie Chart Mesh Controller", EditorStyles.boldLabel);
            EditorGUILayout.Space();
            SerializedProperty pieChartMeshController = serializedObject.FindProperty(GetMemberName(() => script.pieChartMeshController));
            EditorGUILayout.PropertyField(pieChartMeshController);

            script.segments = (int)EditorGUILayout.Slider("Segments", (float)script.segments, 2f, 10f);
            bool updateSegment = false;
            if (GUILayout.Button("Update"))
            {
                updateSegment = true;
            }
            EditorGUILayout.Space();
            EditorGUILayout.Space();
            EditorGUILayout.Space();

            SerializedProperty Data = serializedObject.FindProperty(GetMemberName(() => script.Data));
            if (updateSegment)
                Data.arraySize = script.segments;
            EditorGUILayout.PropertyField(Data, true);
            EditorGUILayout.Space();

            EditorGUILayout.Space();
            EditorGUILayout.Space();
            EditorGUILayout.Space();

            SerializedProperty mainMaterial = serializedObject.FindProperty(GetMemberName(() => script.mainMaterial));
            EditorGUILayout.PropertyField(mainMaterial);
            EditorGUILayout.Space();


            SerializedProperty animationType = serializedObject.FindProperty(GetMemberName(() => script.animationType));
            EditorGUILayout.PropertyField(animationType);
            EditorGUILayout.Space();

            SerializedProperty parentTransform = serializedObject.FindProperty(GetMemberName(() => script.parentTransform));
            EditorGUILayout.PropertyField(parentTransform);
            EditorGUILayout.Space();

            SerializedProperty customColor = serializedObject.FindProperty(GetMemberName(() => script.customColors));
            if (updateSegment)
                customColor.arraySize = script.segments;
            EditorGUILayout.PropertyField(customColor, true);
            EditorGUILayout.Space();

            /*script.justCreateThePie*/
            SerializedProperty justCreateThePie = serializedObject.FindProperty(GetMemberName(() => script.justCreateThePie));
            EditorGUILayout.PropertyField(justCreateThePie);
            //script.justCreateThePie = EditorGUILayout.Toggle("Create Pie Only", script.justCreateThePie);
            script.justCreateThePie = justCreateThePie.boolValue;
            if (!script.justCreateThePie) // if bool is true, show other fields
            {
                SerializedProperty dataDescription = serializedObject.FindProperty(GetMemberName(() => script.dataDescription));
                if (updateSegment)
                    dataDescription.arraySize = script.segments;
                EditorGUILayout.PropertyField(dataDescription, true);
            }
            EditorGUILayout.Space();


            serializedObject.ApplyModifiedProperties();
        }
        public static string GetMemberName<T>(Expression<Func<T>> memberExpression)
        {
            MemberExpression expressionBody = (MemberExpression)memberExpression.Body;
            return expressionBody.Member.Name;
        }


        [MenuItem("ViitorCloud/PieChart/Create")]
        public static void CreatePieChart()
        {
            GameObject go = Instantiate(Resources.Load("PiechartManager") as GameObject);
            go.name = "PiechartManager";
            go.GetComponent<PieChart>().parentTransform = go.transform;
        }
    }
}