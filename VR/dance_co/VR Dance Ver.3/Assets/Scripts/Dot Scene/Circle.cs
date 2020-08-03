using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Circle : MonoBehaviour
{
    public GameObject circle, halfCircle;
    public bool isSize, isSize2, halfCircleColliding;
    public bool moveStart, turns, back, CircleFinish;
    public bool sizes, returnColor, isBlinking, sizeStart;
    public int cnt;

    bool sizeCor1, sizeCor2, sizeCor3;
    bool isTurn, move, sizeMin;

    Ring ring;
    Eye eye;
    
    void Start()
    {
        ring = GameObject.Find("RingManager").GetComponent<Ring>();
        sizeCor1 = sizeCor2 = sizeCor3 = false;
        CircleFinish = false;
        isSize = isSize2 = true;
        back = move = sizes = sizeMin = isBlinking = true;
        returnColor = false;
        halfCircle.SetActive(false);
        circle.SetActive(false);
        turns = false;
        moveStart = sizeStart = false;
        halfCircleColliding = false;
        
        cnt = 0;

        isTurn = false;
        eye = GameObject.Find("EyeManager").GetComponent<Eye>();
    }

    void Update()
    {
        //InCIrcle SIze Up
        if(!sizeCor1 && eye.isBlink)
        {
            circle.SetActive(true);
            StartCoroutine(size());
            sizeCor1 = true;
        }

        //InCircleMove
        if (move && moveStart)
        {
            if (back)
            {
                circle.transform.position = Vector3.MoveTowards(circle.transform.position,
                    new Vector3(circle.transform.position.x, circle.transform.position.y,
                    -2.5f), 1.0f * Time.deltaTime);
         
                if (circle.transform.position.z == -2.5f)
                {
                    back = false;
                }
            }

            else
            {
                circle.transform.position = Vector3.MoveTowards(circle.transform.position,
                    new Vector3(0.6f, 1f, -1), 1.0f * Time.deltaTime);

                if (circle.transform.position == new Vector3(0.6f, 1f, -1) && halfCircleColliding)
                {
                    move = false;
                    circle.transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);
                    circle.transform.position = new Vector3(0, 1f, -1);
                    circle.SetActive(false);
                    halfCircle.SetActive(true);
                    StopCoroutine(size());
                }
            }
        }

        //halfCircle Size Down
        else if(!move && moveStart)
        {
            if (sizes)
            {
                if (!sizeCor2)
                {
                    StartCoroutine(size2());
                    sizeCor2 = true;
                }

                halfCircle.transform.rotation = Quaternion.Slerp(halfCircle.transform.rotation,
                        Quaternion.Euler(0, 0, -140f), 1.0f * Time.deltaTime);

                if(halfCircle.transform.rotation.eulerAngles.z >= 215f && halfCircle.transform.rotation.eulerAngles.z <= 225f)
                {
                    sizes = false;
                }
            }
        }

        //halfCircle Turn
        if(!sizes && turns)
        {
            halfCircle.transform.rotation = Quaternion.Euler(0, 0, -140.0f);
        }

        if(!sizes && !turns)
        {
            halfCircle.transform.rotation = Quaternion.Euler(0, 0, -320.0f);
        }

        if(cnt == 6)
        {
            isTurn = true;
        }

        //halfCircle TUrn Finish;
        if(isTurn && !returnColor)
        {
            circle.SetActive(true);
            returnColor = true;
        }

        if(!isBlinking && !CircleFinish)
        {
            halfCircle.transform.position = Vector3.MoveTowards(halfCircle.transform.position,
                new Vector3(-1.3f, 1f, 0), 0.5f * Time.deltaTime);
            halfCircle.transform.rotation = Quaternion.Slerp(halfCircle.transform.rotation,
                Quaternion.Euler(0, 90f, 160f), 1.0f * Time.deltaTime);

            if (!sizeCor3)
            {
                StartCoroutine(size3());
                sizeCor3 = true;
            }

            if(halfCircle.transform.position == new Vector3(-1.3f, 1f, 0))
            {
                CircleFinish = true;
            }
        }
    }

    IEnumerator size()
    {
        Vector3 scale = new Vector3(0.001f, 0.001f, 0.001f);
        while (isSize)
        {
            circle.transform.localScale += scale;

            if(circle.transform.localScale.x >= 0.25f)
            {
                isSize = false;
            }

            yield return new WaitForSeconds(0.01f);
        }
    }

    IEnumerator size2()
    {
        Vector3 scale = new Vector3(-0.0005f, -0.0005f, -0.0005f);
        while(sizeMin)
        {
            halfCircle.transform.localScale += scale;

            if(halfCircle.transform.localScale.x <= 0.1f)
            {
                sizeMin = false;
            }

            yield return new WaitForSeconds(0.01f);
        }
    }

    IEnumerator size3()
    {
        Vector3 scale = new Vector3(0.001f, 0.001f, 0.001f);
        while (isSize2)
        {
            circle.transform.localScale += scale;

            if (circle.transform.localScale.x >= 0.2f)
            {
                isSize2 = false;
            }

            yield return new WaitForSeconds(0.01f);
        }
    }
}
