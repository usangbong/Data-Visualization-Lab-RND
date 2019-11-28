using System;
using System.Reflection;
using UnityEngine;
using UnityEditor;

namespace UltimateReplay.Editor
{
    [InitializeOnLoad]
    public static class ReplayVariableValidator
    {
        // Constructor
        static ReplayVariableValidator()
        {
            // Validate all replay variables after an AppDomain refresh
            ValidateReplayVariables();
        }

        // Methods
        public static void ValidateReplayVariables()
        {
            // Check all types in 'Assembly-CSharp'
            foreach (Type type in Assembly.GetAssembly(typeof(ReplayVarAttribute)).GetTypes())
            {
                // Get all instance fields
                foreach(FieldInfo field in type.GetFields(BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic))
                {
                    // Check for an attribute
                    if(field.IsDefined(typeof(ReplayVarAttribute), false) == true)
                    {
                        // Make sure the defining class inherits from 'ReplayBehaviour'
                        if(typeof(ReplayBehaviour).IsAssignableFrom(field.DeclaringType) == false)
                        {
                            // Display a warning
                            Debug.LogWarning(string.Format("Field '{0}' defined in type '{1}' is marked with the 'ReplayVarAttribute' but the declaring type does not inherit from 'ReplayBehaviour'. The 'ReplayVarAttribute' will be ignored", field.Name, type.FullName));
                        }
                    }
                }
            }
        }
    }
}
