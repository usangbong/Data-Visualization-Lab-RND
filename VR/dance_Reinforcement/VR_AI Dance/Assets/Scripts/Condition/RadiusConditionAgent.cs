using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class RadiusConditionAgent : Agent
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
        AddVectorObs(moveObject.getOriginPos());
        AddVectorObs(moveObject.getPos());
        AddVectorObs(moveObject.getRadius());
        AddVectorObs(moveObject.getAverageRadius());
        AddVectorObs(select);
    }

    public override void AgentAction(float[] vectorAction)
    {
        select = Mathf.FloorToInt(vectorAction[0]);

        float radius = moveObject.getRadius();
        float averageRadius = moveObject.getAverageRadius();

        if(select == 0)
        {
            if(radius >= averageRadius)
            {
                AddReward(1f);
                cw.correct++;
            }

            else
            {
                AddReward(-1f);
                cw.wrong++;
            }
        }

        else if(select == 1)
        {
            if(radius >= averageRadius)
            {
                AddReward(-1f);
                cw.wrong++;
            }

            else
            {
                AddReward(1f);
                cw.correct++;
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
