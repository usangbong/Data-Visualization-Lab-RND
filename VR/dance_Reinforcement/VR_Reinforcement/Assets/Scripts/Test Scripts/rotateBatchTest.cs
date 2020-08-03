using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;


public class rotateBatchTest : Agent
{
    public Transform target, obj;
    public Transform initialTransform;

    Vector3 targetRotation;

    int cnt = 0;
    public override void OnEpisodeBegin()
    {
        obj.position = initialTransform.position;

        target.position = new Vector3(target.position.x, Random.Range(0f, 2f), target.position.z);
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        sensor.AddObservation(target.position);
        sensor.AddObservation(obj.position);
        sensor.AddObservation(targetRotation);
        sensor.AddObservation(obj.rotation.eulerAngles);
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        int pitch = Mathf.FloorToInt(vectorAction[0]);
        int yaw = Mathf.FloorToInt(vectorAction[1]);
        int roll = Mathf.FloorToInt(vectorAction[2]);
        float speed = Mathf.FloorToInt(vectorAction[3]) * 0.01f;

        targetRotation = new Vector3(pitch, yaw, roll);

        obj.rotation = Quaternion.Euler(targetRotation);
        obj.Translate(Vector3.forward * speed * Time.deltaTime);

        if (target.position.y >= 1.6f)
        {
            if (obj.position.y >= 0.8f) AddReward(0.01f);
            else AddReward(-0.01f);
        }

        else
        {
            if (obj.position.y <= 1.2f) AddReward(0.01f);
            else AddReward(-0.01f);
        }

        if (target.position.x <= -0.5f || target.position.x >= 0.5f)
        {
            if (obj.position.x <= -0.5f || obj.position.x >= 0.5f) AddReward(0.005f);
            else if (obj.position.x > -0.5f && obj.position.x < 0.5f) AddReward(-0.005f);
        }

        else if (target.position.x >= -0.5f && target.position.x <= 0.5f)
        {
            if (obj.position.x >= -0.5f && obj.position.x <= 0.5f) AddReward(0.005f);
            else if (obj.position.x < -0.5f || obj.position.x > 0.5f) AddReward(-0.005f);
        }

        if (target.position.z <= -0.8f || target.position.z >= 0.8f)
        {
            if (obj.position.z < -0.5f || obj.position.z > 0.5f) AddReward(0.005f);
            else if (obj.position.z >= -0.5f && obj.position.z <= 0.5f) AddReward(-0.005f);
        }

        else if(target.position.z >= -0.8f && target.position.z <= 0.8f)
        {
            if (obj.position.z >= -1f && obj.position.z <= 1f) AddReward(0.005f);
            else if (obj.position.z < -1f || obj.position.z > 1f) AddReward(-0.005f);
        }

        Vector3 pos = obj.position;
        if (pos.x >= 1.8f || pos.x <= -1.8f || pos.y >= 2f || pos.y <= 0.2f || pos.z >= 1.2f || pos.z <= -1.2f)
        {
            EndEpisode();
        }
    }
}



/*2번 방법*/
//discrete 범위: 0~360
//그 값으로 x, y, z rotation 좌표

/*3번 방법*/
//continuous 범위 * 360 해서 나온 값 넣기
