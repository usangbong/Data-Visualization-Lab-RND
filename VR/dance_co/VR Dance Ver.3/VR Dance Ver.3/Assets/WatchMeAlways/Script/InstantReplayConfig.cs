using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

namespace WatchMeAlways
{
    // NOTE: InstantReplayConfig must be defined in a separated file, whose filename matches the classname
    // cf. https://answers.unity.com/questions/581460/scriptableobjectcreateinstance-returning-null-valu.html
    public class InstantReplayConfig : ScriptableObject
    {
        const string assetPath = "Assets/WatchMeAlways/InstantReplayConfig.asset";

        public bool AutoStart = false;
        public int Monitor = 0;
        public float ReplayLength = 120;
        public float Fps = 30.0f;
        public InstantReplay.RecordingQuality Quality = InstantReplay.RecordingQuality.MEDIUM;

        protected InstantReplayConfig()
        {

        }

        public static InstantReplayConfig Create()
        {
            return ScriptableObject.CreateInstance<InstantReplayConfig>();
        }

        public static InstantReplayConfig Load()
        {
            var config = UnityEditor.AssetDatabase.LoadAssetAtPath<InstantReplayConfig>(assetPath);
            return config;
        }

        public void CopyFrom(InstantReplayConfig newConfig)
        {
            if (newConfig != null)
            {
                AutoStart = newConfig.AutoStart;
                Monitor = newConfig.Monitor;
                ReplayLength = newConfig.ReplayLength;
                Fps = newConfig.Fps;
                Quality = newConfig.Quality;
            }
        }

        public InstantReplayConfig Save()
        {
            var existingAsset = Load();
            if (existingAsset == null)
            {
                UnityEditor.AssetDatabase.CreateAsset(this, assetPath);
                UnityEditor.AssetDatabase.Refresh();
                existingAsset = this;
            }
            else
            {
                UnityEditor.EditorUtility.CopySerialized(this, existingAsset);
                UnityEditor.AssetDatabase.SaveAssets();
            }
            return existingAsset;
        }
    }
}
