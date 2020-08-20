using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using System.Linq;
using UnityEngine.Serialization;
using System;

public class OfficeAgent : Agent
{
    public OfficeArea area;
    public PlayerMove player;
    public float timeBetweenDecisionsAtInference;
    public Transform obj;
    float m_TimeSinceDecision;

    public Camera renderCamera;
    
    public bool maskActions = true;

    const int k_NoAction = 0;
    const int k_Forward = 1;
    const int k_Back = 2;
    const int k_Left = 3;
    const int k_Right = 4;
    const int k_TurnLeft = 5;
    const int k_TurnRight = 6;

    public override void Initialize()
    {
        area.AreaReset();
        player.resetPos();
    }

    public override void OnEpisodeBegin()
    {

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
        var targetRot = obj.rotation.eulerAngles;
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
            SetReward(-1f);
            EndEpisode();
        }
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
