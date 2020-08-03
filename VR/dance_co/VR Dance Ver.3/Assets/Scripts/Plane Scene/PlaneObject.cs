using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using Valve.VR;

public class PlaneObject : MonoBehaviour
{
    public GameObject left, right, back, front, up, down, grid;
    public GameObject leftB, rightB, backB, frontB, upB, downB;
    public GameObject hide1, hide2, nullPar;
    public GameObject Puzzle1, Puzzle2, Danger;
    public GameObject Background;

    public float time, time2;
    public bool time60, coll;

    List<GameObject> planeList = new List<GameObject>();
    MakeBackground make;
    Vector3 scale;

    bool col, hideObj, func, copy, func2;
    bool InvokeFalse, copyMove, isTime, isTime2;
    bool puzzle2Active, gridActive, puzzle2Move, grideMove, puzzleMove;

    void Start()
    {
        time60 = coll = false;
        col = hideObj = func = copy = func2 = false;
        InvokeFalse = copyMove = isTime = isTime2 = false;
        puzzleMove = puzzle2Move = grideMove = false;
        puzzle2Active = gridActive = false;

        time = time2 = 0f;

        scale = new Vector3(0, -0.01f, 0);
        make = GameObject.Find("GameObject").GetComponent<MakeBackground>();

        Danger.SetActive(false);
    }

    void Update()
    {
        if(make.BackGroundFinish && !time60)
        {
            left.SetActive(true);
            right.SetActive(true);
            up.SetActive(true);
            down.SetActive(true);
            front.SetActive(true);
            back.SetActive(true);
            hide1.SetActive(true);
            hide2.SetActive(true);

            frontB.transform.SetParent(nullPar.transform);
            backB.transform.SetParent(nullPar.transform);
            leftB.transform.SetParent(nullPar.transform);
            rightB.transform.SetParent(nullPar.transform);
            upB.transform.SetParent(nullPar.transform);

            if (!func)
            {
                StartCoroutine(timeChecker());
                func = true;
            }
        }

        if(time60 && !isTime)
        {
            Danger.SetActive(true);
            if(!hideObj)
            {
                hide2.SetActive(false);
                for(int i=0;i<60;i++)
                {
                    if(i<11)
                    {
                        left.transform.GetChild(i).gameObject.SetActive(false);
                    }

                    if(i<18)
                    {
                        right.transform.GetChild(i).gameObject.SetActive(false);
                    }

                    if(i<27)
                    {
                        hide1.transform.GetChild(i).gameObject.SetActive(false);
                    }

                    front.transform.GetChild(i).gameObject.SetActive(false);
                    back.transform.GetChild(i).gameObject.SetActive(false);
                }

                hideObj = true;
            }

            MoveObject(frontB, new Vector3(-0.07f, -0.144f, 1.41f));
            MoveObject(backB, new Vector3(-0.057f, -0.144f, -1.393f));
            MoveObject(leftB, new Vector3(-1.817f, -0.154f, -0.039f));
            MoveObject(rightB, new Vector3(1.676f, -0.144f, -0.024f));
            MoveObject(upB, new Vector3(0f, 2.2f, 0.001f));
            MoveObject(front, new Vector3(-0.44f, -0.039f, 1.926f));
            MoveObject(back, new Vector3(-0.434f, -0.044f, -1.934f));
            MoveObject(left, new Vector3(-2.332f, -0.039f, 0.004f));
            MoveObject(right, new Vector3(2.205f, -0.048f, -0.004f));
            MoveObject(up, new Vector3(-0.4f, 2.1f, 0.002f));
            MoveObject(hide1, new Vector3(2.216f, -0.048f, -0.024f));
            MoveObject(hide2, new Vector3(-2.577f, -0.048f, 0.003f));

            RotateObject(frontB, new Vector3(90, 0, 0));
            RotateObject(backB, new Vector3(-90, 0, 0));
            RotateObject(leftB, new Vector3(90, 90 ,0));
            RotateObject(rightB, new Vector3(90, 90, 0));
            RotateObject(upB, new Vector3(90, 0 ,0));
            RotateObject(front, new Vector3(0, 90, 90));
            RotateObject(back, new Vector3(0, 90, -90));
            RotateObject(left, new Vector3(0, 0, 90));
            RotateObject(right, new Vector3(180, -90, 0));
            RotateObject(up, new Vector3(0, 90, 90));
            RotateObject(hide1, new Vector3(180, 270, 0));
            RotateObject(hide2, new Vector3(0, -90, 0));

            if (frontB.transform.localScale.y >= 0.884f)
            {
                frontB.transform.localScale += scale;
            }

            if (backB.transform.localScale.y >= 0.9238f)
            {
                backB.transform.localScale += scale;
            }

            if (leftB.transform.localScale.y >= 0.8946f)
            {
                leftB.transform.localScale += scale;
            }

            if (rightB.transform.localScale.y >= 0.9177f)
            {
                rightB.transform.localScale += scale;
            }
        }

        if(isTime && !copy)
        {
            upB.SetActive(false);
            frontB.SetActive(false);
            rightB.SetActive(false);
            backB.SetActive(false);
            leftB.SetActive(false);
            hide2.transform.position = new Vector3(0.032f, -0.048f, 0.003f);
            hide2.SetActive(true);

            up.SetActive(false);
            left.SetActive(false);
            right.SetActive(false);
            down.SetActive(false);
            front.SetActive(false);
            back.SetActive(false);

            hide1.SetActive(false);

            copy = true;
        }

        if(copy && !copyMove)
        {
            hide2.transform.position = Vector3.MoveTowards(hide2.transform.position,
                new Vector3(-0.695f, 1.137f, 0.73f), 0.5f * Time.deltaTime);
            hide2.transform.rotation = Quaternion.Slerp(hide2.transform.rotation,
                Quaternion.Euler(-90, 0, 135), 3.0f * Time.deltaTime);

            if (hide2.transform.localScale.y <= 0.15f)
            {
                hide2.transform.localScale += new Vector3(0, 0.005f, 0);
            }

            if(hide2.transform.position.y == 1.137f)
            {
                if(!InvokeFalse)
                {
                    Invoke("hide2ActiveFalse", 10f);
                    Invoke("PuzzleActive", 10f);
                    InvokeFalse = true;
                }
            }
        }

        if(copyMove && !puzzleMove)
        {
            Puzzle1.transform.position = Vector3.MoveTowards(Puzzle1.transform.position,
                new Vector3(-1.642f, 0.365f, 0.279f), 1.0f * Time.deltaTime);

            if(Puzzle1.transform.position == new Vector3(-1.642f, 0.365f, 0.279f))
            {
                puzzleMove = true;

                if(!func2)
                {
                    StartCoroutine(timeChecker2());
                    func2 = true;
                }
            }
        }

        if(!puzzle2Move && puzzle2Active)
        {
            Puzzle2.transform.position = Vector3.MoveTowards(Puzzle2.transform.position,
                new Vector3(1.534f, 1.393f, 0.244f), 1.0F * Time.deltaTime);
            Puzzle2.transform.rotation = Quaternion.Slerp(Puzzle2.transform.rotation,
                Quaternion.Euler(0, -23.095f, 0), 2.0f * Time.deltaTime);

            if(Puzzle2.transform.position == new Vector3(1.534f, 1.393f, 0.244f))
            {
                puzzle2Move = true;
            }
        }

        if(!grideMove && gridActive)
        {
            grid.transform.position = Vector3.MoveTowards(grid.transform.position,
                new Vector3(0.354f, 1.307f, -1.405f), 0.5f * Time.deltaTime);
            grid.transform.rotation = Quaternion.Slerp(grid.transform.rotation,
                Quaternion.Euler(-90, 0, 0), 0.7f * Time.deltaTime);

            if(grid.transform.localScale.x <= 1.5f)
            {
                grid.transform.localScale += new Vector3(0.003f, 0.003f, 0.003f);
            }

            if(grid.transform.position == new Vector3(0.354f, 1.307f, -1.405f))
            {
                Invoke("GridMoveTrue", 5f);
            }
        }

        if(grideMove && !coll)
        {
            Puzzle1.transform.RotateAround(Vector3.zero, Vector3.up, 20f * Time.deltaTime);
            Puzzle2.transform.RotateAround(Vector3.zero, Vector3.up, 20f * Time.deltaTime);
            grid.transform.RotateAround(Vector3.zero, Vector3.up, 20f * Time.deltaTime);
        }
    }

    void MoveObject(GameObject obj, Vector3 toPos)
    {
        obj.transform.position = Vector3.MoveTowards(obj.transform.position,
            toPos, 0.2f * Time.deltaTime);
    }

    void RotateObject(GameObject obj, Vector3 toRot)
    {
        obj.transform.rotation = Quaternion.Slerp(obj.transform.rotation,
            Quaternion.Euler(toRot), 0.5f * Time.deltaTime);
    }

    void PuzzleActive()
    {
        copyMove = true;
        Puzzle1.SetActive(true);
    }

    void hide2ActiveFalse()
    {
        hide2.SetActive(false);
    }

    void GridMoveTrue()
    {
        grideMove = true;
    }

    IEnumerator timeChecker()
    {
        while (!isTime)
        {
            time += 0.1f;
            if (time > 45f)
            {
                time60 = true;
            }

            if(time > 90f)
            {
                isTime = true;
            }

            yield return new WaitForSeconds(0.1f);
        }
    }

    IEnumerator timeChecker2()
    {
        while(!isTime2)
        {
            time2 += 0.1f;

            if(time2 > 7f)
            {
                Puzzle2.SetActive(true);
                puzzle2Active = true;
            }

            if(time2 > 14f)
            {
                grid.SetActive(true);
                gridActive = true;
            }

            if(time2 > 45f)
            {
                coll = true;
            }

            if(time2 > 50f)
            {
                Background.SetActive(true);
                Puzzle1.SetActive(false);
                Puzzle2.SetActive(false);
                grid.SetActive(false);
                col = false;
            }

            if(time2 > 55f)
            {
                isTime2 = true;
                SceneManager.LoadScene("Final_User");
            }

            yield return new WaitForSeconds(0.1f);
        }
    }
}
