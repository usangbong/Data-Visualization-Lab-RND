using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class SpeedConditionAgent : Agent
{
    public GameObject Head;

    CorWrong cw;
    MoveObject moveObject;

    int select;

    private void Awake()
    {
        cw = GameObject.Find("CorWrong").GetComponent<CorWrong>();
        moveObject = Head.GetComponent<MoveObject>();

        StartCoroutine(timeChecker());
    }

    public override void CollectObservations()
    {
        AddVectorObs(moveObject.getVelocity());
        AddVectorObs(moveObject.getAverageVelocity());
        AddVectorObs(select);
    }

    public override void AgentAction(float[] vectorAction)
    {
        select = Mathf.FloorToInt(vectorAction[0]);

        float velocity = moveObject.getVelocity();
        float averageVelocity = moveObject.getAverageVelocity();

        if (select == 0)
        {
            if (velocity >= averageVelocity)
            {
                AddReward(1f);
                cw.correct += 1;
            }

            else
            {
                AddReward(-0.1f);
                cw.wrong += 1;
            }
        }

        else if (select == 1)
        {
            if (velocity >= averageVelocity)
            {
                AddReward(-0.1f);
                cw.wrong += 1;
            }

            else
            {
                AddReward(1f);
                cw.correct += 1;
            }
        }
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
