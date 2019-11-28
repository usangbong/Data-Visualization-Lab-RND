using UnityEngine;
using UnityEditor;

namespace UltimateReplay.Editor
{
    public enum MemoryUnits
    {
        /// <summary>
        ///     Represents a download speed measured in bytes per second.
        /// </summary>
        Bytes,

        /// <summary>
        ///     Represents a download speed measured in kilo bytes per second.
        /// </summary>
        KiloBytes,

        /// <summary>
        ///     Represents a download speed measured in mega bytes per second.
        /// </summary>
        MegaBytes
    }

    public static class ReplayHelper
    {
        // Private
        private const long kiloByteUnit = 1024;
        private const long megaByteUnit = kiloByteUnit * 1024;

        // Methods
        [MenuItem("GameObject/UltimateReplay/Create Replay Controls")]
        public static void CreateReplayControls()
        {
            GameObject go = new GameObject("ReplayControls");

            // Add component
            go.AddComponent<ReplayControls>();

            // Create the object
            Undo.RegisterCreatedObjectUndo(go, "Create Replay Controls");

            // Select the object
            Selection.activeGameObject = go;
        }

        public static decimal GetMemorySize(int amount)
        {
            // Get amount as decimal
            decimal value = amount;

            // Check for mega bytes
            if(value > megaByteUnit)
            {
                // Megabytes
                value = decimal.Round(value / megaByteUnit, 2);
            }
            else if(value > kiloByteUnit)
            {
                // Kilobytes
                value = decimal.Round(value / kiloByteUnit, 2);
            }
            else
            {
                // Bytes should not display a decimal place
                value = decimal.Round(value, 0);
            }

            return value;
        }

        public static MemoryUnits GetMemoryUnit(int amount)
        {
            // Megabytes
            if (amount > megaByteUnit)
                return MemoryUnits.MegaBytes;

            // Kilobytes
            if (amount > kiloByteUnit)
                return MemoryUnits.KiloBytes;

            // Bytes
            return MemoryUnits.Bytes;
        }

        public static string GetMemoryUnitName(int amount)
        {
            switch (GetMemoryUnit(amount))
            {
                case MemoryUnits.Bytes: return "Bytes";
                case MemoryUnits.KiloBytes: return "KB";
                case MemoryUnits.MegaBytes: return "MB";
            }
            return "<?>";            
        }
    }
}
