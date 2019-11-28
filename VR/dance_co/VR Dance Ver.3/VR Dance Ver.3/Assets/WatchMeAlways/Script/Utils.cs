using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace WatchMeAlways
{
    public class Utils
    {
        public static bool CreateDirectoryIfNotExists(string path)
        {
            if (System.IO.Directory.Exists(path))
            {
                return false;
            }
            System.IO.Directory.CreateDirectory(path);
            return true;
        }
    }
}
