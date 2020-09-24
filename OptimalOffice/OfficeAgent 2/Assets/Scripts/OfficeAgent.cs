using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using System.Linq;
using UnityEngine.Serialization;
using System;
using System.IO;

public class OfficeAgent : Agent
{
    public OfficeArea area;
    public PlayerMove player;
    public float timeBetweenDecisionsAtInference;
    public Transform obj;
    float m_TimeSinceDecision;

    int cnt = 0;

    bool begin = false;

    public Camera renderCamera;
    
    public bool maskActions = true;

    const int k_NoAction = 0;
    const int k_Forward = 1;
    const int k_Back = 2;
    const int k_Left = 3;
    const int k_Right = 4;
    
    List<Vector3> posList = new List<Vector3>();

    public override void Initialize()
    {
        Debug.Log(obj.name);
        player.resetPos();
    }

    public override void OnEpisodeBegin()
    {
        cnt = 0;

        if (begin) area.AreaReset();

        begin = true;
    }

    public override void CollectDiscreteActionMasks(DiscreteActionMasker actionMasker)
    {
        if(maskActions)
        {
            var max_posX = 12;
            var min_posX = -12;
            var max_posZ = 7.5f;
            var min_posZ = -7.5f;

            var positionX = Mathf.Round(obj.position.x * 10) * 0.1f;
            var positionZ = Mathf.Round(obj.position.z * 10) * 0.1f;

            if (positionX == min_posX)
            {
                actionMasker.SetMask(0, new[] { k_Left });
            }

            if (positionX == max_posX)
            {
                actionMasker.SetMask(0, new[] { k_Right });
            }

            if (positionZ == min_posZ)
            {
                actionMasker.SetMask(0, new[] { k_Back });
            }

            if (positionZ == max_posZ)
            {
                actionMasker.SetMask(0, new[] { k_Forward });
            }
        }
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        AddReward(0.005f);

        float action = vectorAction[0];

        var targetPos = obj.position;
        switch (action)
        {
            case k_NoAction:
                break;
            case k_Right:
                targetPos = obj.position + new Vector3(0.1f, 0, 0);
                obj.position = targetPos;
                break;
            case k_Left:
                targetPos = obj.position + new Vector3(-0.1f, 0, 0);
                obj.position = targetPos;
                break;
            case k_Forward:
                targetPos = obj.position + new Vector3(0, 0, 0.1f);
                obj.position = targetPos;
                break;
            case k_Back:
                targetPos = obj.position + new Vector3(0, 0, -0.1f);
                obj.position = targetPos;
                break;
            default:
                throw new ArgumentException("Invalid action value");
        }

        if(obj.position.x > 12 || obj.position.x < -12 || obj.position.z > 7.5 || obj.position.z < -7.5)
        {
            SetReward(0f);
            EndEpisode();
        }

        if (player.collidingName() == obj.name)
        {
            AddReward(-0.3f);
        }

        if(cnt>5000)
        {
            SetReward(0f);
            EndEpisode();
        }

        cnt++;
    }

    public void collidingOtherObject()
    {
        AddReward(-0.1f);
    }

    private void FixedUpdate()
    {
        if (renderCamera != null)
        {
            renderCamera.Render();
        }

        if(player.isMoveFinish)
        {
            player.finIdx++;
            if (player.finIdx > 7)
            {
                player.isMoveFinish = false;
                player.finIdx = 0;
            }
            RequestDecision();
        }
    }
}
