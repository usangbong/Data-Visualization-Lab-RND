using UnityEngine;
using UnityEditor;

#if UNITY_5_6_OR_NEWER
using UnityEditor.Build;

public class BuildChecker : IPreprocessBuild
{
    // Properties
    public int callbackOrder
    {
        get { return 0; }
    }

    // Methods
    public void OnPreprocessBuild(BuildTarget target, string path)
    {
        Debug.LogError("The trial version of UltimateReplay cannot be built! Please upgrade to the full version to build your game.");
    }
}
#endif