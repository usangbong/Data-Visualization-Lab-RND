using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

namespace WatchMeAlways
{
    public class Logger
    {
        const string Prefix = ""; // "WatchMeAlways: ";

        public static void Info(string format, params object[] args)
        {
            Debug.LogFormat(Prefix + format, args);
        }

        public static void Warn(string format, params object[] args)
        {
            Debug.LogWarningFormat(Prefix + format, args);
        }

        public static void Error(string format, params object[] args)
        {
            Debug.LogErrorFormat(Prefix + format, args);
        }
    }
}
