using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class HeightConditionAgent : Agent
{
    public GameObject Head;

    CorWrong cw;
    MoveObject moveObject;

    int select = -1;

    void Awake()
    {
        cw = GameObject.Find("CorWrong").GetComponent<CorWrong>();
        moveObject = Head.GetComponent<MoveObject>();

        StartCoroutine(timeChecker());
    }

    public override void CollectObservations()
    {
        AddVectorObs(moveObject.getYpos());
        AddVectorObs(select);
    }

    public override void AgentAction(float[] vectorAction)
    {
        select = Mathf.FloorToInt(vectorAction[0]);

        float yPos = moveObject.getYpos();

        if (select == 0)
        {
            if (yPos >= 1.65f)
            {
                cw.correct += 1;
                AddReward(1f);
            }

            else
            {
                cw.wrong += 1;
                AddReward(-1f);
            }
        }

        else if (select == 1)
        {
            if (yPos >= 1.65f)
            {
                cw.wrong += 1;
                AddReward(-1f);
            }

            else
            {
                cw.correct += 1;
                AddReward(1f);
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
