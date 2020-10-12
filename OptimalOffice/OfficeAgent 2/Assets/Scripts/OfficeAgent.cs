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
    public Transform obj;

    public Camera renderCamera;
   
    public override void Initialize()
    {

    }

    public override void OnEpisodeBegin()
    {

    }

    public override void OnActionReceived(float[] vectorAction)
    {
        float action = vectorAction[0];

        Cell cell = area.FindCell(System.Convert.ToInt32(action));

        transform.position = cell.getObjectPos(gameObject);
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
