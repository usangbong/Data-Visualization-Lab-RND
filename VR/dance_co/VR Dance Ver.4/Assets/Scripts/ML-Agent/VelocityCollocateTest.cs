using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class VelocityCollocateTest : Agent
{
    public Transform pivot, target;

    Vector3 lastPosition, currentPosition;

    IntegratedCorWrong cw;
    CollocateManager cm;

    float averageVelocity = 0, velocity;
    float timeStep = 0.02f, distance;

    int countVelocity = 0, select;

    void Awake()
    {
        cw = GameObject.Find("CorWrong").GetComponent<IntegratedCorWrong>();
        cm = GameObject.Find("setObjectManager").GetComponent<CollocateManager>();

        StartCoroutine(timeChecker());
    }

    public override void CollectObservations()
    {
        AddVectorObs(velocity);
        AddVectorObs(averageVelocity);
        AddVectorObs(select);
    }

    public override void AgentAction(float[] vectorAction)
    {
        select = Mathf.FloorToInt(vectorAction[0]);

        currentPosition = target.position;

        distance = Vector3.Distance(lastPosition, currentPosition);
        velocity = distance / timeStep;
        averageVelocity = averageVelocity + (velocity - averageVelocity) / ++countVelocity;

        if(select == 0)
        {
            if(velocity >= averageVelocity)
            {
                cw.vCorrect++;
                cm.setFast(true);
                AddReward(1f);
            }

            else
            {
                cw.vWrong++;
                cm.setFast(false);
                AddReward(-1f);   
            }
        }

        else if(select == 1)
        {
            if(velocity >= averageVelocity)
            {
                cw.vWrong++;
                cm.setFast(true);
                AddReward(-1f);
            }

            else
            {
                cw.vCorrect++;
                cm.setFast(false);
                AddReward(1f);
            }
        }

        lastPosition = currentPosition;
    }

    public void setLastPosition(Vector3 pos)
    {
        lastPosition = pos;
    }

    IEnumerator timeChecker()
    {
        while (true)
        {
            yield return new WaitForSeconds(100f);

            cw.change = true;
            Done();
        }
    }
}
