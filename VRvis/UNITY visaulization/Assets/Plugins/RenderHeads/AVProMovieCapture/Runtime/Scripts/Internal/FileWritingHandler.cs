//-----------------------------------------------------------------------------
// Copyright 2012-2020 RenderHeads Ltd.  All rights reserved.
//-----------------------------------------------------------------------------

namespace RenderHeads.Media.AVProMovieCapture
{
	/// Allows the user to monitor a capture that has completed, but the file is still being written to asynchronously
	public class FileWritingHandler : System.IDisposable
	{
		private string _path;
		private int _handle;

		public string Path
		{
			get { return _path; }
		}

		internal FileWritingHandler(string path, int handle)
		{
			_path = path;
			_handle = handle;
		}

		public bool IsFileReady()
		{
			bool result = true;
			if (_handle >= 0)
			{
				result = NativePlugin.IsFileWritingComplete(_handle);
				if (result)
				{
					Dispose();
				}
			}
			return result;
		}

		public void Dispose()
		{
			if (_handle >= 0)
			{
				NativePlugin.FreeRecorder(_handle);
				_handle = -1;
			}
		}
	}
}