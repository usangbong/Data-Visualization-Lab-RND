using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;

public class HeightSpeedBatchTest : Agent
{
    public Transform target, obj;
    public Transform InitialTransform;

    public WideXBatchTest wideX;
    public WideZBatchTest wideZ;

    public float speed = 0.1f;

    float time = 0;

    public override void Initialize()
    {
        StartCoroutine(timeChecker());
    }

    public override void OnEpisodeBegin()
    {
        target.transform.position = new Vector3(Random.Range(-1.5f, 1.5f),
                    Random.Range(1.3f, 2), Random.Range(-1f, 1f));
        obj.position = InitialTransform.position;
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        sensor.AddObservation(target.position.y);
        sensor.AddObservation(obj.position.y);
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        int tall = Mathf.FloorToInt(vectorAction[0]);
        int isUp = Mathf.FloorToInt(vectorAction[1]);

        if (tall == 0)
        {
            if (isUp == 1) obj.Translate(Vector3.up * speed * Time.deltaTime);
            else obj.Translate(Vector3.down * speed * Time.deltaTime);
        }

        else
        {
            if (isUp == 1) obj.Translate(Vector3.up * speed * Time.deltaTime);
            else obj.Translate(Vector3.down * speed * Time.deltaTime);
        }

        if (obj.position.y > 2f || obj.position.y < 0f)
        {
            time = 0;
            AddReward(-1f);
            EndEpisode();
        }

        else
        {
            CheckUpDown(tall);
        }
    }

    IEnumerator timeChecker()
    {
        while(true)
        {
            time += 1f;

            if(time >= 50f)
            {
                time = 0;
                wideX.EndEpisode();
                wideZ.EndEpisode();
                EndEpisode();
            }

            yield return new WaitForSeconds(1f);
        }
    }

    void CheckUpDown(int isTall)
    {
        if(target.position.y >= 1.6f)
        {
            if (obj.position.y >= 0.8f)
            {
                if (isTall == 1) AddReward(0.005f);
                else AddReward(-0.005f);
            }

            else
            {
                AddReward(-0.005f);
            }
        }

        else 
        {
            if (obj.position.y <= 1.2f)
            {
                if (isTall == 0) AddReward(0.005f);
                else AddReward(-0.005f);
            }

            else
            {
                AddReward(-0.005f);
            }
        }
    }
}
