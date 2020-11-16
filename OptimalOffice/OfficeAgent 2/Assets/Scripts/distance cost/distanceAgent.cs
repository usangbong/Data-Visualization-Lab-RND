using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;

public class distanceAgent : Agent
{
    public Transform Objects;


    public override void OnEpisodeBegin()
    {
        
    }

    public override void CollectObservations(VectorSensor sensor)
    {
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        for(var i=0;i<Objects.childCount;i++)
        {
            float action = vectorAction[i];

            GameObject obj = Objects.GetChild(i).gameObject;
            
        }
    }
}
