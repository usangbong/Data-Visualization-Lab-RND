using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;

public class WideXBatchTest : Agent
{
    public Transform target, obj, heightBatch;
    public Transform InitialTransform;

    public float speed = 0.1f;

    HeightSpeedBatchTest hTest;

    public override void Initialize()
    {
        hTest = heightBatch.GetComponent<HeightSpeedBatchTest>();
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        sensor.AddObservation(target.position.x);
        sensor.AddObservation(obj.position.x);
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        int xWide = Mathf.FloorToInt(vectorAction[0]);
        int moveRight = Mathf.FloorToInt(vectorAction[1]);

        if (moveRight == 1) obj.Translate(Vector3.right * speed * Time.deltaTime);
        else obj.Translate(Vector3.left * speed * Time.deltaTime);

        if (obj.position.x > 1.7f || obj.position.x < -1.7f)
        {
            AddReward(-1f);
            hTest.EndEpisode();
        }

        else
        {
            CheckUpDown(xWide);
        }
    }

    void CheckUpDown(int isWideX)
    {
        if(target.position.x >= 0.8f || target.position.x <= -0.8f)
        {
            if(obj.position.x >= 0.8f || obj.position.x <= -0.8f)
            {
                if (isWideX == 1) AddReward(0.005f);
                else AddReward(-0.005f);
            }

            else if(obj.position.z > -0.8f && obj.position.z < 0.8f)
            {
                AddReward(-0.005f);
            }
        }

        else if(target.position.x > -0.8f && target.position.x <0.8f)
        {
            if (obj.position.x > -0.8f && obj.position.x < 0.8f)
            {
                if (isWideX == 1) AddReward(-0.005f);
                else AddReward(0.005f);
            }

            else if(obj.position.x >= 0.8f || obj.position.x <= -0.8f)
            {
                AddReward(-0.005f);
            }
        }
    }
}
