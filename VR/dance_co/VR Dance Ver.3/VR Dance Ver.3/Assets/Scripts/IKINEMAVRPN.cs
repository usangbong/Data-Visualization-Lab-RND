// Copyright © 2019, IKINEMA Ltd. All rights reserved.
// IKINEMA VRPN SDK, source distribution
// Your use and or redistribution of this software in source and / or binary form, with or without modification, is subject to: 
// 1. your ongoing acceptance of and compliance with the terms and conditions of the IKINEMA License Agreement; and 
// 2. your inclusion of this notice in any version of this software that you use  or redistribute.
// A copy of the IKINEMA License Agreement is available by contacting IKinema Ltd., https://www.ikinema.com, support@ikinema.com

using System;
using System.Collections.Generic;
using UnityEngine;

namespace IKINEMAClient
{
	/// <summary>
	/// Basic component that drives the parent hierarchy from an IKINEMA VRPN stream
	/// </summary>
    [AddComponentMenu("Mocap/IKINEMA VRPN")]
    public class IKINEMAVRPN : MonoBehaviour
    {
        public const string Version = "0.5";

        // Editor settings
        [Tooltip("Subject name as set in Orion output options")]
        public string SubjectName = "Skeleton";
        [Tooltip("Address:port of the machine running Orion")]
        public string ServerHost = "localhost:3883";
        [Tooltip("Apply the stream scale factor to this game object")]
        public bool UpdateScaleFromStream = true;
		[Tooltip("Applies vertical 180 deg rotation internally to match SteamVR plugin")]
		public bool ApplyVerticalRotation = true;

        // old stream properties
        [Header("Compatibility settings")]
        public bool IsStreamYUp = true;
        public float InputScale = 0.01F;

        public void Start()
        {
            var connectionString = SubjectName + "@" + ServerHost;
            m_client = StreamCharacter.Connect(connectionString);
        }

        public void Update()
        {
            UpdateTransformsFromStream();
        }

        // implementation
        protected StreamCharacter m_client = null;
        private bool m_isMetadataRead = false;
        private uint m_rootId = uint.MaxValue;
        private List<Transform> m_streamHierarchy = null;
        private Quaternion ZtoY = new Quaternion(0.7071F, 0, 0, 0.7071F);
		private Quaternion Vertical180 = new Quaternion(0, 1, 0, 0);

        private void ReadMetadata()
        {
            try
            {
                m_streamHierarchy = new List<Transform>();
                uint streamBoneCount = m_client.GetBoneCount();
				Dictionary<string, Transform> gameObjectHierarchy = ReadGameObjectHierarchy();

                for (uint boneId = 0U; boneId < streamBoneCount; boneId++)
                {
                    string boneName = m_client.GetBoneName(boneId);
                    m_streamHierarchy.Add(gameObjectHierarchy[boneName]);

                    string parentName = m_client.GetParentBoneName(boneId);
                    if (parentName.Length == 0)
                        m_rootId = boneId;
                }

                m_isMetadataRead = true;
            }
            catch (KeyNotFoundException)
            {
                Debug.LogError("Streamed bones not part of this asset");
            }
            catch (Exception e)
            {
                Debug.Log(e.Message);
            }
        }

        private void UpdateTransformsFromStream()
        {
            if (m_client == null || !m_client.IsInitialized())
                return;

            // we need to have the metadata to process the data
            if (!m_isMetadataRead)
                ReadMetadata();
            
            if (!m_client.GetFrame())
            {
                Debug.Log("Unable to read a new frame");
                return;
            }

            // update GameObject scale
            if (UpdateScaleFromStream)
            {
                float figureScale = m_client.GetFigureScale();
                transform.localScale = new Vector3(figureScale, figureScale, figureScale);
            }

            // update individual bones
            for (uint boneId = 0U; boneId < m_streamHierarchy.Count; boneId++)
            {
                TransformData data = m_client.GetBoneLocalTransform(boneId);
                Transform boneTransform = m_streamHierarchy[(int)boneId];

                Vector3 streamTransaltion = ParseVector(ref data) * InputScale;
                Quaternion streamRotation = ParseQuaternion(ref data);
                
				// root only modifications
				if (boneId == m_rootId) {
					// output = VerticalRot * ZtoYRot * input
	                if (!IsStreamYUp) 
	                {
	                    // rotate root to match non Zup stream to Unity
	                    streamTransaltion = ZtoY * streamTransaltion;
	                    streamRotation = ZtoY * streamRotation;
	                }

					if (ApplyVerticalRotation) 
					{
						streamTransaltion = Vertical180 * streamTransaltion;
						streamRotation = Vertical180 * streamRotation;
					}
				}

                boneTransform.localPosition = streamTransaltion;
                boneTransform.localRotation = streamRotation;
            }
        }

        private Dictionary<string, Transform> ReadGameObjectHierarchy()
        {
            // Create an ordered list using the frame bone order from the metadata
            var hierarchy = new Dictionary<string, Transform>();
            var transformsToVisit = new Stack<Transform>();
            
            // push all children of the root transform
            for (int childIndex = 0; childIndex < transform.childCount; childIndex++)
                transformsToVisit.Push(transform.GetChild(childIndex));

            while (transformsToVisit.Count > 0)
            {
                Transform currentTransform = transformsToVisit.Pop();
                try
                {
                    hierarchy.Add(currentTransform.name, currentTransform);
                }
                catch (ArgumentException)
                {
                    Debug.LogWarning("Element with duplicate name: " + currentTransform.name);
                }

                for (int childIndex = 0; childIndex < currentTransform.childCount; childIndex++)
                    transformsToVisit.Push(currentTransform.GetChild(childIndex));
            }
            return hierarchy;
        }

        protected Vector3 ParseVector(ref TransformData inputData)
        {
            // do transformations needed from VRPN to Unity coordinate system
            return new Vector3(-inputData.position[0], inputData.position[1], inputData.position[2]);
        }

        protected Quaternion ParseQuaternion(ref TransformData inputData)
        {
            // do transformations needed from VRPN to Unity coordinate system
            return new Quaternion(inputData.orientation[0], -inputData.orientation[1], -inputData.orientation[2], inputData.orientation[3]);
        }
    }
}
