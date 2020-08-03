using System.Collections;
using System.Collections.Generic;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using UnityEngine;

using System.IO;

public class HeightBatchTest : Agent
{
    public Transform target, obj;

    const float MAX_POINT = 2f, MIN_POINT = 0.2f, H_POINT = 1.6f;
    const float TALL_POINT = 0.8f, SHORT_POINT = 1.2f;

    public int correct = 0, wrong = 0;

    bool moveFinish = true;

    public float yPos;
    float updatevalue, updateYpos;
    int cnt = 0;

    public override void Initialize()
    {
        StartCoroutine(timeChecker());
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        sensor.AddObservation(yPos);
        sensor.AddObservation(target.position.y >= H_POINT);
        sensor.AddObservation(target.position.y < H_POINT);

        sensor.AddObservation(target.position.y);
        sensor.AddObservation(obj.position.y);
    }

    public override void OnActionReceived(float[] vectorAction)
    {
        updateYpos = Mathf.Abs(vectorAction[0]) * 2f;

        if(target.position.y < H_POINT) {
            updatevalue = Mathf.Abs(vectorAction[1]) * (1.2f - updateYpos);
        }
        else {
            updatevalue = Mathf.Abs(vectorAction[1]) * (updateYpos - 0.8f);
        }

        if (target.position.y >= H_POINT)
        {
            yPos = updateYpos - updatevalue;
        }
        else
        {
            yPos = updateYpos + updatevalue;
        }
        
        yPos = Mathf.Round(yPos * 1000) * 0.001f;
        
        Vector3 originPos = obj.transform.position;

        if (moveFinish)
        {
            moveFinish = false;
            StartCoroutine(MoveObject(yPos, originPos));
        }

        CheckUpDown(yPos);
    }
    
    IEnumerator MoveObject(float yPos, Vector3 originPos)
    {
        Vector3 targetPos = new Vector3(originPos.x, yPos, originPos.z);

        while (!moveFinish)
        {
            obj.transform.position = Vector3.MoveTowards(obj.transform.position,
                targetPos, 1.0f * Time.deltaTime);

            yield return new WaitForSeconds(Time.deltaTime);

            if (obj.transform.position == targetPos)
            {
                moveFinish = true;

                int tall = Random.Range(0, 2);

                target.transform.position = new Vector3(target.transform.position.x,
                    Random.Range(1.3f, 2), target.transform.position.z);
            }
        }
    }

    IEnumerator timeChecker()
    {
        float time = 0;
        while(true)
        {
            time += 0.1f;

            if(time >= 30f)
            {
                time = 0;
                EndEpisode();
            }

            yield return new WaitForSeconds(0.1f);
        }
    }

    public override void OnEpisodeBegin()
    {
        cnt++;
        Debug.Log(obj.name + " " + cnt + "Time\n" + "correct: " + correct + " wrong: " + wrong);
        correct = wrong = 0;
    }

    void CheckUpDown(float yPos)
    {
        if (target.transform.position.y >= H_POINT) //Tall
        {
            if (yPos >= TALL_POINT)
            {
                AddReward(1f);
                correct++;
            }
            else
            {
                AddReward(-1f);
                wrong++;
            }
        }

        else
        {
            if (yPos >= SHORT_POINT)
            {
                AddReward(-1f);
                wrong++;
            }
            else
            {
                AddReward(1f);
                correct++;
            }
        }
    }
}
