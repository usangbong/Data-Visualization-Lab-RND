// Copyright © 2019, IKINEMA Ltd. All rights reserved.
// IKINEMA VRPN SDK, source distribution
// Your use and or redistribution of this software in source and / or binary form, with or without modification, is subject to: 
// 1. your ongoing acceptance of and compliance with the terms and conditions of the IKINEMA License Agreement; and 
// 2. your inclusion of this notice in any version of this software that you use  or redistribute.
// A copy of the IKINEMA License Agreement is available by contacting IKinema Ltd., https://www.ikinema.com, support@ikinema.com

using System;
using System.Runtime.InteropServices;

namespace IKINEMAClient
{
    [StructLayout(LayoutKind.Sequential, Pack = 1)]
    public struct TransformData {
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 3)]
        public float[] position;
        [MarshalAs(UnmanagedType.ByValArray, SizeConst = 4)]
        public float[] orientation;
    }

    public class StreamCharacter
    {
        /// <summary>
        /// Factory method that return a StreamCharacter connected to the given VRPN address
        /// </summary>
        /// <param name="connectionString">VRPN formated connection string <example>Skeleton@localhost:3883</example></param>
        static public StreamCharacter Connect(string connectionString)
        {
            return new StreamCharacter(connectionString);
        }

        private StreamCharacter(string connectionString)
        {
            m_nativeHandle = CharacterCreate(connectionString);
            if (m_nativeHandle == IntPtr.Zero)
                throw new InvalidProgramException("Unable to initialize VRPN client to " + connectionString);

            // marshalling buffers
            m_nameBuffer = Marshal.AllocHGlobal(NativeStringLength);
            m_transformBuffer = Marshal.AllocHGlobal(Marshal.SizeOf(typeof(TransformData)));
        }

        ~StreamCharacter()
        {
            CharacterDestroy(m_nativeHandle);
            m_nativeHandle = IntPtr.Zero;

            if (m_nameBuffer != IntPtr.Zero) {
                Marshal.FreeHGlobal(m_nameBuffer);
                m_nameBuffer = IntPtr.Zero;
            }

            if (m_transformBuffer != IntPtr.Zero) {
                Marshal.FreeHGlobal(m_transformBuffer);
                m_transformBuffer = IntPtr.Zero;
            }
        }

        /// <summary>
        /// Checks internal client state
        /// </summary>
        /// <returns>true if the character if the metadata has been received from the server</returns>
        public bool IsInitialized()
        {
            return CharacterInitialized(m_nativeHandle);
        }

        /// <summary>
        /// Returns global actor scale
        /// </summary>
        public float GetFigureScale()
        {
            return CharacterFigureScale(m_nativeHandle);
        }

        /// <summary>
        /// Returns true if animation data is available
        /// </summary>
        public bool GetFrame()
        {
            return GetFrame(m_nativeHandle);
        }

        // bones
        public uint GetBoneCount()
        {
            return GetBoneCount(m_nativeHandle);
        }

        public string GetBoneName(uint boneId)
        {
            GetBoneName(m_nativeHandle, boneId, m_nameBuffer, NativeStringLength);
            return Marshal.PtrToStringAnsi(m_nameBuffer);
        }

        public string GetParentBoneName(uint boneId)
        {
            GetParentBoneName(m_nativeHandle, boneId, m_nameBuffer, NativeStringLength);
            return Marshal.PtrToStringAnsi(m_nameBuffer);
        }

        public TransformData GetBoneRestLocalTransform(uint boneId)
        {
            GetBoneRestLocalTransform(m_nativeHandle, boneId, m_transformBuffer);
            return (TransformData)Marshal.PtrToStructure(m_transformBuffer, typeof(TransformData));
        }

        public TransformData GetBoneLocalTransform(uint boneId)
        {
            GetBoneLocalTransform(m_nativeHandle, boneId, m_transformBuffer);
            return (TransformData)Marshal.PtrToStructure(m_transformBuffer, typeof(TransformData));
        }

        // rigid bodies
        public uint GetRigidBodyCount()
        {
            return GetRigidBodyCount(m_nativeHandle);
        }

        public string GetRigidBodyName(uint rigidBodyId)
        {
            GetRigidBodyName(m_nativeHandle, rigidBodyId, m_nameBuffer, NativeStringLength);
            return Marshal.PtrToStringAnsi(m_nameBuffer);
        }

        public TransformData GetRigidBodyGlobalTransform(uint rigidBodyId)
        {
            GetRigidBodyGlobalTransform(m_nativeHandle, rigidBodyId, m_transformBuffer);
            return (TransformData)Marshal.PtrToStructure(m_transformBuffer, typeof(TransformData));
        }

        // //////////////////////////////////////////////////////////////////////////////
        // implementation details
        // //////////////////////////////////////////////////////////////////////////////
        private IntPtr m_nativeHandle = IntPtr.Zero;
        private const string NativeDLL = "IKinemaVRPN_C";
        private const int NativeStringLength = 64;
        private IntPtr m_nameBuffer = IntPtr.Zero;
        private IntPtr m_transformBuffer = IntPtr.Zero;

        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern IntPtr CharacterCreate([MarshalAs(UnmanagedType.LPStr)]string connectionString);

        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern void CharacterDestroy(IntPtr nativeHandle);

        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern bool CharacterInitialized(IntPtr nativeHandle);

        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern float CharacterFigureScale(IntPtr nativeHandle);

        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern bool GetFrame(IntPtr nativeHandle);

        // bones
        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern uint GetBoneCount(IntPtr nativeHandle);

        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern void GetBoneName(IntPtr nativeHandle, uint boneId, IntPtr resultBuffer, uint bufferLength);

        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern void GetParentBoneName(IntPtr nativeHandle, uint boneId, IntPtr resultBuffer, uint bufferLength);

        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern void GetBoneRestLocalTransform(IntPtr nativeHandle, uint boneId, IntPtr resultBuffer);

        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern void GetBoneLocalTransform(IntPtr nativeHandle, uint boneId, IntPtr resultBuffer);

        // rigid bodies
        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern uint GetRigidBodyCount(IntPtr nativeHandle);

        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern void GetRigidBodyName(IntPtr nativeHandle, uint rigidBodyId, IntPtr resultBuffer, uint bufferLength);

        [DllImport(NativeDLL, CallingConvention = CallingConvention.Cdecl)]
        static private extern void GetRigidBodyGlobalTransform(IntPtr nativeHandle, uint rigidBodyId, IntPtr resultBuffer);
    }
}
