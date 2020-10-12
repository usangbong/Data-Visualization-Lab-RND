﻿//========= Copyright 2018, HTC Corporation. All rights reserved. ===========
using System.Runtime.InteropServices;
using UnityEngine;
using UnityEngine.Assertions;

namespace ViveSR
{
    namespace anipal
    {
        namespace Eye
        {
            public class SRanipal_GazeRaySample_v2 : MonoBehaviour
            {
                public Vector3 start, last;
                public Vector3 Llast;
                public Vector3 Rlast;

                public int LengthOfRay = 25;
                [SerializeField] private LineRenderer GazeRayRenderer;
                private static EyeData_v2 eyeData = new EyeData_v2();
                private bool eye_callback_registered = false;
                private void Start()
                {
                    if (!SRanipal_Eye_Framework.Instance.EnableEye)
                    {
                        enabled = false;
                        return;
                    }
                    Assert.IsNotNull(GazeRayRenderer);
                }

                private void Update()
                {
                    if (SRanipal_Eye_Framework.Status != SRanipal_Eye_Framework.FrameworkStatus.WORKING &&
                        SRanipal_Eye_Framework.Status != SRanipal_Eye_Framework.FrameworkStatus.NOT_SUPPORT) return;

                    if (SRanipal_Eye_Framework.Instance.EnableEyeDataCallback == true && eye_callback_registered == false)
                    {
                        SRanipal_Eye_v2.WrapperRegisterEyeDataCallback(Marshal.GetFunctionPointerForDelegate((SRanipal_Eye_v2.CallbackBasic)EyeCallback));
                        eye_callback_registered = true;
                    }
                    else if (SRanipal_Eye_Framework.Instance.EnableEyeDataCallback == false && eye_callback_registered == true)
                    {
                        SRanipal_Eye_v2.WrapperUnRegisterEyeDataCallback(Marshal.GetFunctionPointerForDelegate((SRanipal_Eye_v2.CallbackBasic)EyeCallback));
                        eye_callback_registered = false;
                    }

                    Vector3 GazeOriginCombinedLocal, GazeDirectionCombinedLocal;
                    Vector3 GazeOriginLeftLocal, GazeDirectionLeftLocal;
                    Vector3 GazeOriginRightLocal, GazeDirectionRightLocal;

                    if (eye_callback_registered)
                    {
                        if (SRanipal_Eye_v2.GetGazeRay(GazeIndex.COMBINE, out GazeOriginCombinedLocal, out GazeDirectionCombinedLocal, eyeData)) {}
                        else if (SRanipal_Eye_v2.GetGazeRay(GazeIndex.LEFT, out GazeOriginCombinedLocal, out GazeDirectionCombinedLocal, eyeData)) {}
                        else if (SRanipal_Eye_v2.GetGazeRay(GazeIndex.RIGHT, out GazeOriginCombinedLocal, out GazeDirectionCombinedLocal, eyeData)) {}
                        else return;
                        //
                        if (SRanipal_Eye_v2.GetGazeRay(GazeIndex.LEFT, out GazeOriginLeftLocal, out GazeDirectionLeftLocal, eyeData)) { }
                        if (SRanipal_Eye_v2.GetGazeRay(GazeIndex.RIGHT, out GazeOriginRightLocal, out GazeDirectionRightLocal, eyeData)) { }
                    }
                    else
                    {
                        if (SRanipal_Eye_v2.GetGazeRay(GazeIndex.COMBINE, out GazeOriginCombinedLocal, out GazeDirectionCombinedLocal)) { }
                        else if (SRanipal_Eye_v2.GetGazeRay(GazeIndex.LEFT, out GazeOriginCombinedLocal, out GazeDirectionCombinedLocal)) { }
                        else if (SRanipal_Eye_v2.GetGazeRay(GazeIndex.RIGHT, out GazeOriginCombinedLocal, out GazeDirectionCombinedLocal)) { }
                        else return;
                        // 
                        if (SRanipal_Eye_v2.GetGazeRay(GazeIndex.LEFT, out GazeOriginLeftLocal, out GazeDirectionLeftLocal, eyeData)) { }
                        if (SRanipal_Eye_v2.GetGazeRay(GazeIndex.RIGHT, out GazeOriginRightLocal, out GazeDirectionRightLocal, eyeData)) { }
                    }


                    start = Camera.main.transform.position - Camera.main.transform.up * 0.05f;
                    Vector3 GazeDirectionCombined = Camera.main.transform.TransformDirection(GazeDirectionCombinedLocal);
                    GazeRayRenderer.SetPosition(0, start);
                    GazeRayRenderer.SetPosition(1, Camera.main.transform.position + GazeDirectionCombined * LengthOfRay);
                    last = Camera.main.transform.position + GazeDirectionCombined * LengthOfRay;

                    Vector3 GazeDirectionLeft = Camera.main.transform.TransformDirection(GazeDirectionLeftLocal);
                    Llast = Camera.main.transform.position + GazeDirectionLeft * LengthOfRay;

                    Vector3 GazeDirectionRight = Camera.main.transform.TransformDirection(GazeDirectionRightLocal);
                    Rlast = Camera.main.transform.position + GazeDirectionRight * LengthOfRay;

                }
                private void Release()
                {
                    if (eye_callback_registered == true)
                    {
                        SRanipal_Eye_v2.WrapperUnRegisterEyeDataCallback(Marshal.GetFunctionPointerForDelegate((SRanipal_Eye_v2.CallbackBasic)EyeCallback));
                        eye_callback_registered = false;
                    }
                }
                private static void EyeCallback(ref EyeData_v2 eye_data)
                {
                    eyeData = eye_data;
                }
            }
        }
    }
}
