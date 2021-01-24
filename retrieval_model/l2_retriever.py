import re


def extract_the_answer(question_dict, db_refrence):
    # extract the answer like : <basic_courses> , <advanced_courses>(mvvm)
    # form the answer sentence and replace it by its true url or string from the database
    final_answer = question_dict["answer"]
    exctracted_quotes = re.findall(r"<\w+>[\(\w+\)]*", final_answer)
    for quote in exctracted_quotes:
        # extract the actual quote
        # example : <basic_courses> -> basic_courses
        clearified_quoute = re.findall("<(\w+)>", quote)[0]
        # extract the name of the set which contains the informations
        # such as : basic_courses -> courses
        set_name = clearified_quoute.split("_")[-1]
        answer_document = db_refrence.collection(
            question_dict["collection"]).document(clearified_quoute).get().to_dict()
        # this to check if there is a parameter is based to the statement
        # like : <advanced_courses>(mvvm) and then extarct it
        has_parameter = re.search("\(\w+\)", quote)
        db_answers = ""
        if has_parameter:
            exctracted_parameter = re.findall("\((\w+)\)", quote)[0]
            for ans_key in answer_document[set_name]:
                if exctracted_parameter in ans_key:
                    db_answers += "\n {}".format(
                        answer_document[set_name][ans_key])

        else:
            for ans_key in answer_document[set_name]:
                db_answers += "\n {} : {} ".format(ans_key,
                                                   answer_document[set_name][ans_key])
        if db_answers == "":
            final_answer = "Error somehow could't find anything from the database"
        else:
            final_answer = final_answer.replace(quote, db_answers)

    return final_answer
