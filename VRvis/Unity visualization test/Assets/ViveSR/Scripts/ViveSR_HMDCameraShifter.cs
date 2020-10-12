//========= Copyright 2017, HTC Corporation. All rights reserved. ===========

using UnityEngine;

namespace Vive.Plugin.SR
{
    public class ViveSR_HMDCameraShifter : MonoBehaviour
    {
        [SerializeField] private Camera TargetCamera;
        public Vector3 CameraShift = Vector3.zero;

        private void Update()
        {
            transform.localPosition =
                CameraShift.x * TargetCamera.transform.right +
                CameraShift.y * TargetCamera.transform.up +
                CameraShift.z * TargetCamera.transform.forward;
        }
    }
}