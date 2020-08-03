using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class UpDownConditionAgent : Agent
{
    public Transform pivot, target;

    float originYpos, diffYpos;
    int select;

    CorWrong cw;

    private void Awake()
    {
        cw = GameObject.Find("CorWrong").GetComponent<CorWrong>();

        StartCoroutine(timeChecker());

        originYpos = target.position.y;
    }

    public override void CollectObservations()
    {
        AddVectorObs(originYpos);
        AddVectorObs(target.transform.position.y);
        AddVectorObs(diffYpos);
        AddVectorObs(select);
    }

    public override void AgentAction(float[] vectorAction)
    {
        select = Mathf.FloorToInt(vectorAction[0]);

        diffYpos = originYpos - target.transform.position.y;
        diffYpos = Mathf.Round(diffYpos * 100) * 0.01f;

        if (select == 0)
        {
            if (diffYpos <= originYpos * 0.7f)
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

        else if (select == 1)
        {
            if (diffYpos > originYpos * 0.7f)
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
