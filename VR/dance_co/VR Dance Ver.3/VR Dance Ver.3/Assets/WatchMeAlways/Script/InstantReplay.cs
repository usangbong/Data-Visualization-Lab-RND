using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using System.Runtime.InteropServices;

namespace WatchMeAlways
{
    public class InstantReplay : Singleton<InstantReplay>
    {
        readonly string serverPath = System.IO.Path.GetFullPath("./Assets/WatchMeAlways/Plugins/x86_64/WatchMeAlwaysServer.exe");
        readonly string ffmpegPath = System.IO.Path.GetFullPath("./Assets/WatchMeAlways/Plugins/x86_64/ffmpeg.exe");

        public static string GalleryDicrectory
        {
            // The full path of folder where recorded video will be saved.
            get
            {
                string documentRoot = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
                string path = System.IO.Path.Combine(documentRoot, "WatchMeAlways");
                path = System.IO.Path.Combine(path, "Gallery");
                return path;
            }
        }

        public static string TmpDicrectory
        {
            get
            {
                string documentRoot = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
                string path = System.IO.Path.Combine(documentRoot, "WatchMeAlways");
                path = System.IO.Path.Combine(path, "tmp");
                return path;
            }
        }

        public static string LogDicrectory
        {
            get
            {
                string documentRoot = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
                string path = System.IO.Path.Combine(documentRoot, "WatchMeAlways");
                path = System.IO.Path.Combine(path, "log");
                return path;
            }
        }

        public static string MessageFile
        {
            get
            {
                string path = System.IO.Path.Combine(TmpDicrectory, "msg.txt");
                return path;
            }
        }

        InstantReplayConfig config_ { get; set; }

        public void Start()
        {
            if (System.IO.Directory.Exists(TmpDicrectory))
            {
                foreach (var f in System.IO.Directory.GetFiles(TmpDicrectory))
                {
                    System.IO.File.Delete(f);
                }
            }

            killAll(serverPath);

            string arg = "";
            if (config_ != null)
            {
                arg += " --monitor " + config_.Monitor;
                arg += " --length " + config_.ReplayLength;
                arg += " --fps " + config_.Fps;
                arg += " --quality " + config_.Quality.ToString();
            }
            arg += " --msgpath " + MessageFile;

            int pid = System.Diagnostics.Process.GetCurrentProcess().Id;
            arg += " --parentpid " + pid;

            runServer(arg);

            if (config_ != null)
            {
                Logger.Info(
                    "Start InstantReplay\n" +
                    "Monitor: MONITOR{0}, " +
                    "ReplayLength: {1}, " +
                    "Fps: {2}, " +
                    "Quality: {3}\n" +
                    "MessageFile: {4}, " +
                    "ThisProcessId: {5}",
                    config_.Monitor,
                    config_.ReplayLength,
                    config_.Fps,
                    config_.Quality,
                    MessageFile,
                    pid
                );
            }
            else
            {
                Logger.Info(
                    "Start InstantReplay\n" +
                    "MessageFile: {0}, " +
                    "ThisProcessId: {1}",
                    MessageFile,
                    pid
                );
            }
        }

        public void Stop()
        {
            killAll(serverPath);
            Logger.Info("Stop InstantReplay");
        }

        System.Diagnostics.Process ffmpegProcess = null;

        public void Save()
        {
            Utils.CreateDirectoryIfNotExists(GalleryDicrectory);
            Utils.CreateDirectoryIfNotExists(TmpDicrectory);

            string basepath = System.IO.Path.Combine(GalleryDicrectory, DateTime.Now.ToString("yyyyMMdd-HHmmss"));
            string h264path = basepath + ".h264";
            bool ok = sendMessage("@save " + h264path);
            if (!ok)
            {
                Logger.Error("Failed to encode video");
                return;
            }

            string mp4path = basepath + ".mp4";
            if (ffmpegProcess != null && ffmpegProcess.HasExited == false)
            {
                kill(ffmpegProcess);
            }

            ffmpegProcess = runFFmpeg(string.Format("-i {0} -c:v copy -f mp4 -y {1}", h264path, mp4path));
            if (ffmpegProcess == null)
            {
                Logger.Error("Failed to covert h264 to mp4");
                return;
            }
            ffmpegProcess.WaitForExit(10 * 1000);

            // Delete
            System.IO.File.Delete(h264path);

            // TODO: progress bar?
            
            Logger.Info("Saved last {0} minutes {1} secs\nSaved in {2}\n\n{3}\n{4}", ffmpegVideoTime.Minutes, ffmpegVideoTime.Seconds, mp4path, ffmpegError, ffmpegLog);
        }

        public InstantReplayConfig GetConfig()
        {
            if (config_ == null)
            {
                config_ = InstantReplayConfig.Load();
            }

            var config = InstantReplayConfig.Create();
            config.CopyFrom(config_);
            return config;
        }

        public void ApplyConfig(InstantReplayConfig newConfig)
        {
            if (config_ == null)
            {
                config_ = InstantReplayConfig.Create();
            }

            if (newConfig != null)
            {
                config_.CopyFrom(newConfig);
                config_.Save();

                // if (IsRecording())
                {
                    // restart
                    Stop();
                    Start();
                }
            }
        }


        public bool IsRecording()
        {
            return search(serverPath).Count >= 1;
        }

        public void GetMonitors()
        {
            List<Monitor> monitors = new List<Monitor>();
            int count = GetMonitorCount();
            for (int i = 0; i < count; i++)
            {
                var m = new Monitor();
                int err = GetMonitor(i, m);
                if (err != 0)
                {
                    Logger.Warn("Failed to get information of monitor " + i);
                    continue;
                }
                monitors.Add(m);
            }
        }

        void killAll(string path)
        {
            var processes = search(path);
            foreach (var p in processes)
            {
                kill(p);
            }
        }

        List<System.Diagnostics.Process> search(string path)
        {
            try
            {
                string processName = System.IO.Path.GetFileNameWithoutExtension(path).ToLower();
                var allProcesses = System.Diagnostics.Process.GetProcesses();
                var processes = allProcesses.Where(p =>
                {
                    return p.ProcessName.ToLower() == processName;
                }).ToList();
                return processes;
            }
            catch (Exception ex)
            {
                Logger.Error("search: " + ex.ToString() + "\n" + ex.StackTrace);
            }
            return new List<System.Diagnostics.Process>();
        }

        System.Diagnostics.Process runServer(string arguments)
        {
            try
            {
                var process = System.Diagnostics.Process.Start(serverPath, arguments);
                return process;
            }
            catch (Exception ex)
            {
                Logger.Error("run: " + ex.ToString() + "\n" + ex.StackTrace);
            }
            return null;
        }

        string ffmpegLog = "";
        string ffmpegError = "";
        TimeSpan ffmpegVideoTime = TimeSpan.Zero;

        System.Diagnostics.Process runFFmpeg(string arguments)
        {
            try
            {
                var startInfo = new System.Diagnostics.ProcessStartInfo(ffmpegPath)
                {
                    CreateNoWindow = true,
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    Arguments = arguments,
                };

                var process = new System.Diagnostics.Process();
                process.StartInfo = startInfo;
                process.Start();

                // hook output
                ffmpegLog = "";
                ffmpegError = "";
                ffmpegVideoTime = TimeSpan.Zero;
                process.OutputDataReceived += (obj, args) => ffmpegLog += args.Data + "\n";
                process.ErrorDataReceived += (obj, args) =>
                {
                    parseFFmpegStdError(args.Data);
                    ffmpegError += args.Data + "\n";
                };
                process.BeginOutputReadLine();
                process.BeginErrorReadLine();

                return process;
            }
            catch (Exception ex)
            {
                Logger.Error("run: " + ex.ToString() + "\n" + ex.StackTrace);
            }

            return null;
        }

        readonly System.Text.RegularExpressions.Regex ffmepgTimeRegex = new System.Text.RegularExpressions.Regex(@"(?<hour>\d\d):(?<min>\d\d):(?<sec>\d\d).\d\d");
        void parseFFmpegStdError(string text)
        {
            var tokens = text.Split(' ');
            foreach (string tkn in tokens)
            {
                const string prefix = "time=";
                if (tkn.StartsWith(prefix))
                {
                    var mc = ffmepgTimeRegex.Match(tkn);
                    if (mc.Success)
                    {
                        int h, m, s;
                        if (
                            int.TryParse(mc.Groups["hour"].Value, out h) &&
                            int.TryParse(mc.Groups["min"].Value, out m) &&
                            int.TryParse(mc.Groups["sec"].Value, out s))
                        {
                            ffmpegVideoTime = new TimeSpan(h, m, s);
                        }
                    }
                }
            }
        }

        void kill(System.Diagnostics.Process process)
        {
            try
            {
                if (process != null && process.HasExited == false)
                {
                    process.Kill();
                    process.WaitForExit(1000);
                }
            }
            catch (Exception ex)
            {
                Logger.Error("kill: " + ex.ToString() + "\n" + ex.StackTrace);
            }
        }

        bool sendMessage(string msg)
        {
            string tokenPath = System.IO.Path.Combine(TmpDicrectory, Guid.NewGuid().ToString());
            System.IO.File.WriteAllText(MessageFile, msg + " " + tokenPath);
            int cnt = 0;
            while (true)
            {
                bool ok = System.IO.File.Exists(tokenPath);
                if (ok) break;

                if (cnt++ > 3000)
                {
                    return false; // timeout (3000ms)
                }

                System.Threading.Thread.Sleep(1);
            }
            return true;
        }

        [StructLayout(LayoutKind.Sequential)]
        public class Monitor
        {
            public int Left = 0;
            public int Top = 0;
            public int Width = 0;
            public int Height = 0;
            public bool IsPrimary = false;
        };

        [DllImport("WatchMeAlwaysLib")]
        public static extern int GetMonitorCount();

        [DllImport("WatchMeAlwaysLib")]
        public static extern int GetMonitor(int n, [Out] Monitor monitor);

        public enum RecordingQuality
        {
            ULTRAFAST = 0,
            SUPERFAST,
            VERYFAST,
            FASTER,
            FAST,
            MEDIUM, // default
            SLOW,
            SLOWER,
            VERYSLOW,
        };
    }
}
