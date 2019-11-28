using UnityEngine;

namespace WatchMeAlways
{
    // cf. http://waken.hatenablog.com/entry/2016/03/05/102928
    public class Singleton<T> where T: class, new()
    {
        private static readonly T instance_ = new T();

        protected Singleton()
        {
            Debug.Assert(null == instance_);
        }

        public static T Instance
        {
            get
            {
                return instance_;
            }
        }
    }
}